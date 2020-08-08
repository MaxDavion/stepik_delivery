from preload_data import reader
from models.categories import Category
from models.meals import Meal
from models import db

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