import unittest
from app import app


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def login(self):
        with self.client.session_transaction() as session:
            session["username"] = "admin"

    def test_login_valid_credentials(self):
        response = self.client.post(
            "/users/login",
            data={"username": "admin", "password": "password"},
            follow_redirects=True
        )
        self.assertEqual(response.request.path, "/users/profile")
        self.assertIn("Welcome, admin!", response.get_data(as_text=True))

    def test_profile_requires_login(self):
        response = self.client.get("/users/profile", follow_redirects=True)
        self.assertEqual(response.request.path, "/users/login")

    def test_add_and_delete_cookie(self):
        self.login()

        self.client.post("/users/cookies/add", data={"key": "color", "value": "red", "max_age": "60"})
        self.assertEqual(self.client.get_cookie("color").value, "red")

        self.client.post("/users/cookies/delete", data={"key": "color"})
        self.assertIsNone(self.client.get_cookie("color"))

    def test_change_theme(self):
        self.login()

        self.client.get("/users/theme/light")
        self.assertEqual(self.client.get_cookie("theme").value, "light")

        response = self.client.get("/users/profile")
        self.assertIn('data-bs-theme="light"', response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
