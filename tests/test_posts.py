import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post


class PostsCrudTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # ---------- helpers ----------

    def make_post(self, **fields):
        data = {
            "title": "First post",
            "content": "Some content",
            "category": "news",
            "posted": datetime(2026, 1, 15, 12, 0),
            "is_active": True,
        }
        data.update(fields)
        post = Post(**data)
        db.session.add(post)
        db.session.commit()
        return post.id

    def get_post(self, post_id):
        # the view committed through its own session state, so drop cached objects first
        db.session.expire_all()
        return db.session.get(Post, post_id)

    def form_data(self, **changes):
        data = {
            "title": "New post",
            "content": "Post body",
            "is_active": "y",
            "publish_date": "2026-03-01T09:30",
            "category": "tech",
        }
        data.update(changes)
        return data

    def login(self, username="arsen"):
        with self.client.session_transaction() as session:
            session["username"] = username

    # ---------- create ----------

    def test_create_page_shows_form(self):
        response = self.client.get("/post/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="title"', response.get_data(as_text=True))

    def test_create_post(self):
        response = self.client.post("/post/create", data=self.form_data())
        self.assertEqual(response.status_code, 302)

        post = db.session.scalars(db.select(Post)).one()
        self.assertEqual(post.title, "New post")
        self.assertEqual(post.content, "Post body")
        self.assertEqual(post.category, "tech")
        self.assertTrue(post.is_active)
        self.assertEqual(post.posted, datetime(2026, 3, 1, 9, 30))

    def test_create_post_anonymous_author(self):
        self.client.post("/post/create", data=self.form_data())
        post = db.session.scalars(db.select(Post)).one()
        self.assertEqual(post.author, "Anonymous")

    def test_create_post_session_user_is_author(self):
        self.login("arsen")
        self.client.post("/post/create", data=self.form_data())
        post = db.session.scalars(db.select(Post)).one()
        self.assertEqual(post.author, "arsen")

    def test_create_post_inactive(self):
        data = self.form_data()
        del data["is_active"]  # unchecked checkbox is simply not sent
        self.client.post("/post/create", data=data)
        post = db.session.scalars(db.select(Post)).one()
        self.assertFalse(post.is_active)

    def test_create_post_invalid_data(self):
        response = self.client.post("/post/create", data=self.form_data(title=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db.session.scalars(db.select(Post)).all(), [])

    # ---------- list ----------

    def test_list_shows_only_active_posts(self):
        self.make_post(title="Visible post")
        self.make_post(title="Hidden post", is_active=False)

        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn("Visible post", text)
        self.assertNotIn("Hidden post", text)

    def test_list_newest_first(self):
        self.make_post(title="Older post", posted=datetime(2026, 1, 1, 8, 0))
        self.make_post(title="Newer post", posted=datetime(2026, 2, 1, 8, 0))

        text = self.client.get("/post").get_data(as_text=True)
        self.assertLess(text.index("Newer post"), text.index("Older post"))

    # ---------- detail ----------

    def test_detail_post(self):
        post_id = self.make_post(title="Detail title", content="Full detail content", author="arsen")

        response = self.client.get(f"/post/{post_id}")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn("Detail title", text)
        self.assertIn("Full detail content", text)
        self.assertIn("arsen", text)

    def test_detail_missing_post_404(self):
        response = self.client.get("/post/999")
        self.assertEqual(response.status_code, 404)

    # ---------- update ----------

    def test_edit_page_prefilled(self):
        post_id = self.make_post(title="Old title")

        response = self.client.get(f"/post/{post_id}/update")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn("Old title", text)
        self.assertIn("2026-01-15", text)  # publish_date filled from post.posted

    def test_edit_post(self):
        post_id = self.make_post(title="Old title")

        data = self.form_data(title="Updated title", category="other", publish_date="2026-05-20T18:45")
        del data["is_active"]
        response = self.client.post(f"/post/{post_id}/update", data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], f"/post/{post_id}")

        post = self.get_post(post_id)
        self.assertEqual(post.title, "Updated title")
        self.assertEqual(post.category, "other")
        self.assertFalse(post.is_active)
        self.assertEqual(post.posted, datetime(2026, 5, 20, 18, 45))

    def test_edit_post_invalid_data(self):
        post_id = self.make_post(title="Old title")

        response = self.client.post(f"/post/{post_id}/update", data=self.form_data(title=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_post(post_id).title, "Old title")

    def test_edit_missing_post_404(self):
        response = self.client.get("/post/999/update")
        self.assertEqual(response.status_code, 404)

    # ---------- delete ----------

    def test_delete_confirm_page(self):
        post_id = self.make_post(title="Post to delete")

        response = self.client.get(f"/post/{post_id}/delete")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Post to delete", response.get_data(as_text=True))
        self.assertIsNotNone(self.get_post(post_id))  # GET must not delete

    def test_delete_post(self):
        post_id = self.make_post()

        response = self.client.post(f"/post/{post_id}/delete")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/post")
        self.assertIsNone(self.get_post(post_id))

    def test_delete_missing_post_404(self):
        response = self.client.post("/post/999/delete")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
