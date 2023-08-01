from django.urls import path

from . import views

urlpatterns = [
    path("mypet/", views.mypet, name="mypet")
   
]