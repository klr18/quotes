from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rating/<str:sample>/', views.rating, name='rating'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('add_source/', views.add_source, name='add_source'),
    path('like/<int:pk>/', views.like, name='like'),
    path('dislike/<int:pk>/', views.dislike, name='dislike'),
]