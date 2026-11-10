import io
import tempfile
import unittest
from pathlib import Path

from app import app
from app.products import products_bp
from app.products.db import get_products_table


class ProductsCrudTestCase(unittest.TestCase):

    def setUp(self):
        # temporary db and uploads folder, so the real data/products.json is never touched
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = Path(self.tmp.name)
        (tmp_path / "static" / "uploads").mkdir(parents=True)

        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.old_db = app.config["PRODUCTS_DB"]
        self.old_static = products_bp.static_folder
        app.config["PRODUCTS_DB"] = tmp_path / "products.json"
        products_bp.static_folder = str(tmp_path / "static")

        self.client = app.test_client()

    def tearDown(self):
        app.config["PRODUCTS_DB"] = self.old_db
        products_bp.static_folder = self.old_static
        app.config["WTF_CSRF_ENABLED"] = True
        self.tmp.cleanup()

    def form_data(self, **changes):
        data = {
            "name": "Keyboard",
            "content": "Mechanical keyboard",
            "price": "49.99",
            "category": "other",
            "quantity": "10",
        }
        data.update(changes)
        return data

    def get_product(self, product_id):
        with app.app_context():
            return get_products_table().get(doc_id=product_id)

    def test_add_product(self):
        response = self.client.post("/products/add", data=self.form_data())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/products/1")

        product = self.get_product(1)
        self.assertEqual(product["name"], "Keyboard")
        self.assertEqual(product["price"], 49.99)
        self.assertEqual(product["quantity"], 10)
        self.assertEqual(product["image"], "")
        self.assertIn("created_at", product)

    def test_add_product_invalid_data(self):
        response = self.client.post("/products/add", data=self.form_data(name="ab", price="-5"))
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        self.assertIn("Field must be at least 3 characters long.", data)
        self.assertIsNone(self.get_product(1))

    def test_list_and_detail_pages(self):
        self.client.post("/products/add", data=self.form_data())

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Keyboard", response.get_data(as_text=True))

        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mechanical keyboard", response.get_data(as_text=True))

        self.assertEqual(self.client.get("/products/999").status_code, 404)

    def test_image_upload(self):
        data = self.form_data(image=(io.BytesIO(b"fake png"), "photo.PNG"))
        self.client.post("/products/add", data=data)

        image = self.get_product(1)["image"]
        self.assertTrue(image.startswith("uploads/"))
        self.assertTrue(image.endswith(".png"))
        self.assertTrue(Path(products_bp.static_folder, image).exists())

        data = self.form_data(image=(io.BytesIO(b"fake gif"), "anim.gif"))
        response = self.client.post("/products/add", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.get_product(2))

    def test_edit_product(self):
        self.client.post("/products/add", data=self.form_data(image=(io.BytesIO(b"png"), "a.png")))
        before = self.get_product(1)

        response = self.client.post("/products/1/edit", data=self.form_data(name="Mouse", price="19.50"))
        self.assertEqual(response.status_code, 302)

        after = self.get_product(1)
        self.assertEqual(after["name"], "Mouse")
        self.assertEqual(after["price"], 19.5)
        self.assertEqual(after["created_at"], before["created_at"])
        self.assertEqual(after["image"], before["image"])

    def test_delete_product(self):
        self.client.post("/products/add", data=self.form_data(image=(io.BytesIO(b"png"), "a.png")))
        image_path = Path(products_bp.static_folder, self.get_product(1)["image"])

        self.assertEqual(self.client.get("/products/1/delete").status_code, 405)

        response = self.client.post("/products/1/delete")
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.get_product(1))
        self.assertFalse(image_path.exists())


if __name__ == "__main__":
    unittest.main()
