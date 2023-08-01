from django.contrib.auth import authenticate  
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin  

# Register your models here.

@admin.register(Friends)
class Friend(admin.ModelAdmin):
    list_display =['id','name','hobby','photo','gender','dob']
    
class CustomUserAdmin(UserAdmin):   
    model = Users  
  
    list_display = ('email', 'is_staff', 'is_available',)  
    list_filter = ('email', 'is_staff', 'is_available',)  
    fieldsets = (  
        (None, {'fields': ('email', 'password','name','dob','contact_no','gender')}),  
        ('Permissions', {'fields': ('is_staff', 'is_available')}),  
    )  
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_available')}  
        ),  
    )  
    search_fields = ('email',)  
    ordering = ('email',)  
    filter_horizontal = ()  
  
admin.site.register(Users, CustomUserAdmin)  