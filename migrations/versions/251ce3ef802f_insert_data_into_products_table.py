"""Insert data into products table

Revision ID: 251ce3ef802f
Revises: 60f82fb3a1bc
Create Date: 2026-11-18 16:24:32.727563

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column

# revision identifiers, used by Alembic.
revision = '251ce3ef802f'
down_revision = '60f82fb3a1bc'
branch_labels = None
depends_on = None


def upgrade():
    # --- Описи таблиць для bulk_insert ---
    categories_table = table('categories', column('id', sa.Integer), column('name', sa.String))

    products_table = table('products',
        column('name', sa.String),
        column('price', sa.Float),
        column('active', sa.Boolean),
        column('category_id', sa.Integer),
    )

    # --- Вставка категорій ---
    op.bulk_insert(categories_table, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'},
    ])

    # --- Вставка продуктів ---
    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True, 'category_id': 2},
        {'name': 'Smartphone LG', 'price': 800.0, 'active': True, 'category_id': 2},
        {'name': 'Novel', 'price': 20.0, 'active': True, 'category_id': 3},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False, 'category_id': 4},
    ])

def downgrade():
   # Видаляємо тільки ці вставлені продукти та категорії

   # Видаляємо продукти по назвах
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone LG', 'Novel', 'T-Shirt');
    """)

    # Видаляємо категорії по назвах
    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)