from django.urls import path,include
from . import views 
urlpatterns = [
    path("", views.home, name="home"),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('register/',views.RegisterUser.as_view(),name='register'),
    path('logout/',views.logout_user,name='logout'),
    path("add/", views.add_index, name="add_index"),
    path("add_friend/", views.add_friend, name="add_friend"),
    path("list/", views.list_friend, name="list"),
    path("update_user/", views.update_user, name="update_user"),
    path("search_user/", views.search_user, name="search_user"),
    path("update", views.update, name="update"),
    path("delete_user", views.delete_user, name="delete"),
    path("calculator/", views.calculator, name="calculator"),
    path("total_sum/", views.total_sum, name="total_sum"),
]
