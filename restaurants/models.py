from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating from 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.restaurant.name}"

class DietaryTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dietary_tags = models.ManyToManyField(DietaryTag, blank=True)

    def __str__(self):
        return self.name

class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Discount code (e.g., STUDENT20)
    description = models.TextField()  # Description of the discount
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage discount (e.g., 20.00)
    is_active = models.BooleanField(default=True)  # Whether the discount is active
    valid_from = models.DateTimeField()  # Start date of the discount
    valid_to = models.DateTimeField()  # End date of the discount

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}% off"