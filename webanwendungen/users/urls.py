"""Defines URL patterns for users"""

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    # Schließt Standard-Authentifizierungs-URLs ein.
    path('', include('django.contrib.auth.urls')),
    # Registrierungsseite
    path('register/', views.register, name='register'),
]
