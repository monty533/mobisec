from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(MyPet)
class MyPet(admin.ModelAdmin):
    list_display =['name','image_url']
    