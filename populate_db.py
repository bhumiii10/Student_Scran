import os
import django
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_scran.settings')
django.setup()

from restaurants.models import Restaurant, MenuItem, DietaryTag, Discount


def populate_db():
    # Create dietary tags
    veg, _ = DietaryTag.objects.get_or_create(name='Vegetarian')
    vegan, _ = DietaryTag.objects.get_or_create(name='Vegan')
    non_veg, _ = DietaryTag.objects.get_or_create(name='Non-Vegetarian')

    # Create restaurants and menu items
    restaurants = [
        {
            "name": "Green Bites",
            "location": "123 Main St, Cityville",
            "description": "A cozy vegetarian restaurant offering healthy and delicious meals.",
            "menu": [
                {"name": "Vegetable Stir Fry", "price": 12.99, "tags": [veg]},
                {"name": "Cheese Pizza", "price": 10.99, "tags": [veg]},
            ],
        },
        {
            "name": "Burger Haven",
            "location": "456 Elm St, Townsville",
            "description": "A popular spot for juicy burgers and fries.",
            "menu": [
                {"name": "Classic Cheeseburger", "price": 8.99, "tags": [non_veg]},
                {"name": "Veggie Burger", "price": 7.99, "tags": [veg]},
            ],
        },
        {
            "name": "Vegan Delight",
            "location": "789 Oak St, Vegantown",
            "description": "A vegan-friendly restaurant with a variety of plant-based dishes.",
            "menu": [
                {"name": "Vegan Buddha Bowl", "price": 11.99, "tags": [vegan]},
                {"name": "Tofu Tacos", "price": 9.99, "tags": [vegan]},
            ],
        },
        {
            "name": "Pasta Palace",
            "location": "111 Pasta Ave, Foodville",
            "description": "Delicious pasta dishes for all dietary preferences.",
            "menu": [
                {"name": "Spaghetti Carbonara", "price": 13.99, "tags": [non_veg]},
                {"name": "Margherita Pizza", "price": 9.99, "tags": [veg]},
            ],
        },
        {
            "name": "Sushi Spot",
            "location": "222 Sushi Blvd, Seaview",
            "description": "Fresh sushi and rolls to satisfy your cravings.",
            "menu": [
                {"name": "California Roll", "price": 14.99, "tags": [vegan]},
                {"name": "Salmon Sashimi", "price": 16.99, "tags": [non_veg]},
            ],
        },
        {
            "name": "Curry Corner",
            "location": "333 Curry Lane, Spicetown",
            "description": "Authentic curry dishes with rich flavors.",
            "menu": [
                {"name": "Chicken Tikka Masala", "price": 12.99, "tags": [non_veg]},
                {"name": "Vegetable Biryani", "price": 10.99, "tags": [veg]},
            ],
        },
        {
            "name": "Taco Town",
            "location": "444 Taco Street, Flavortown",
            "description": "Tacos for every taste bud.",
            "menu": [
                {"name": "Beef Tacos", "price": 8.99, "tags": [non_veg]},
                {"name": "Bean and Cheese Tacos", "price": 7.99, "tags": [veg]},
            ],
        },
        {
            "name": "Pizza Planet",
            "location": "555 Pizza Way, Cheesetown",
            "description": "Your go-to spot for delicious pizzas.",
            "menu": [
                {"name": "Pepperoni Pizza", "price": 11.99, "tags": [non_veg]},
                {"name": "Veggie Supreme Pizza", "price": 10.99, "tags": [veg]},
            ],
        },
    ]

    for restaurant_data in restaurants:
        restaurant, _ = Restaurant.objects.get_or_create(
            name=restaurant_data["name"],
            location=restaurant_data["location"],
            description=restaurant_data["description"],
        )
        for item in restaurant_data["menu"]:
            menu_item, _ = MenuItem.objects.get_or_create(
                restaurant=restaurant,
                name=item["name"],
                price=item["price"],
            )
            menu_item.dietary_tags.set(item["tags"])

    print("Database populated successfully!")

    # Add a single discount
    Discount.objects.create(
        code="STUDENT20",
        description="20% off for students",
        discount_percentage=20.00,
        is_active=True,
        valid_from=timezone.now(),
        valid_to=timezone.now() + timezone.timedelta(days=365),  # Valid for 1 year
    )

if __name__ == '__main__':
    populate_db()

