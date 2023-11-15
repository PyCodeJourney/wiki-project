from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.choose_random, name="random"),
    path("search/", views.search, name="search"),
    path("<str:title>", views.entry, name="entry"),
    path("create/", views.create_entry, name="create"),
    path("edit/<str:title>", views.edit_entry, name="edit")
]
