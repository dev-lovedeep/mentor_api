from django.contrib import admin

# Register your models here.
from .models import UserProfile,Tags

admin.site.register([UserProfile,Tags])
