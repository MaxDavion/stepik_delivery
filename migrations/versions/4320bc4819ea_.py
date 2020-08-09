"""empty message

Revision ID: 4320bc4819ea
Revises: 
Create Date: 2020-08-09 14:34:45.816961

"""
from alembic import op
import sqlalchemy as sa
from preload_data import reader
from models.categories import Category
from models.meals import Meal
from models import db

# revision identifiers, used by Alembic.
revision = '4320bc4819ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('picture', sa.String(length=100), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders_meals',
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('meal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meal_id'], ['meals.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], )
    )
    # ### end Alembic commands ###
    categories = []
    for category in reader.load_categories():
        categories.append(
            Category(
                id=category['id'],
                title=category['title']
            ))

    meals = []
    for meal in reader.load_meals():
        meals.append(
            Meal(
                id=meal['id'],
                title=meal['title'],
                price=meal['price'],
                description=meal['description'],
                picture=meal['picture'],
                category=[category for category in categories if category.id == meal['category_id']][0]
            ))

    db.session.add_all(categories)
    db.session.add_all(meals)
    db.session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders_meals')
    op.drop_table('orders')
    op.drop_table('meals')
    op.drop_table('categories')
    op.drop_table('accounts')
    # ### end Alembic commands ###