from django.urls import path

from . import views

# app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("createNew/", views.createNew, name="createNew"),
    path("editPage/", views.editPage, name="editPage"),
    path("rendomPage/", views.rendomPage, name="rendomPage"),
    
]
