import unittest

from app import create_app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        self.assertIn("JOHN", data)
        self.assertIn("30", data)

    def test_admin_page(self):
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        self.assertIn("ADMIN", data)
        self.assertIn("42", data)


if __name__ == "__main__":
    unittest.main()