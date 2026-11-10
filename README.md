# Lab 5: WTForms

A Flask app with forms built on Flask-WTF. The contact form validates its fields, is protected from CSRF, writes every message to `logs/contacts.log` and follows the Post/Redirect/Get pattern. The `products` blueprint stores products in TinyDB (`data/products.json`) and supports adding, viewing, editing and deleting them, with image uploads saved to `app/products/static/uploads/`. All form fields are rendered with a shared macro that shows the field's errors, and every action shows a flash message.

## Screenshots

### Contact form validation
![Contact form validation](.github/assets/lab5/form_fail.png)

### Contact form submitted
![Contact form submitted](.github/assets/lab5/form_submission.png)

### Products page
![Products page](.github/assets/lab5/products_page.png)

### Product page
![Product page](.github/assets/lab5/product_page.png)

### Product form validation
![Product form validation](.github/assets/lab5/product_invalid.png)

### Delete confirmation
![Delete confirmation](.github/assets/lab5/delete_dialog.png)
