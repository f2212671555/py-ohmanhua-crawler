from django.urls import path
from crawler import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search", views.search_comic, name="search"),
    path("show/<str:name>/<str:href>/<str:version>", views.show_comic, name="show"),
    path("read/<str:name>/<str:href>/<str:title>/<str:version>", views.read_comic, name="read"),
]