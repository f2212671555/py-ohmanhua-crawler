from django.urls import path
from crawler import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search", views.search_comic, name="search"),
    path("show", views.show_comic, name="show"),
    path("read", views.read_comic, name="read"),
]