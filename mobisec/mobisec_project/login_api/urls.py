from django.urls import path,include
from . import views 

# Document ---->  These login  api will call from postman Thank you

urlpatterns = [
    path('register_user/', views.RegisterUser.as_view(), name='register'),
    path('login_user/', views.UserLogin.as_view(), name='login_user'),
    path('fetch_user/', views.FetchUser.as_view(), name='fetch_user')
]