from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

# Register CustomUser model
admin.site.register(CustomUser)
