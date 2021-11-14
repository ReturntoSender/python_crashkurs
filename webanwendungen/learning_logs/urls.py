"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'

urlpatterns = [
    # Startseite
    path('', views.index, name='index'),
    # Seite, die alle Fachgebiete anzeigt.
    path('topics/', views.topics, name='topics'),
    # Seite für ein einzelnes Fachgebiet
    path('topics/<int:topic_id>/', views.topic, name='topic'),
]
