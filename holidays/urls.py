"""URL patterns for the holidays app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/holidays/', views.get_holidays, name='get_holidays'),
]
