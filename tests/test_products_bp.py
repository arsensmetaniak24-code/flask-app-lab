import unittest
from app import app


class ProductsBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_all_products_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        self.assertIn("All Products", data)
        self.assertIn("Laptop", data)
        self.assertIn("Phone", data)
        self.assertIn("PC", data)

    def test_product_detail_page(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        self.assertIn("Laptop", data)
        self.assertIn("1200", data)
        self.assertIn("Intel Core i7", data)


if __name__ == "__main__":
    unittest.main()