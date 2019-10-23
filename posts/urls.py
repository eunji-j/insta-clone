from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('hashtags/<int:id>/', views.hashtags, name="hashtags"),
    path('<int:id>/like/', views.like, name="like"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/comment/create/', views.comment_create, name="comment_create"),
]
