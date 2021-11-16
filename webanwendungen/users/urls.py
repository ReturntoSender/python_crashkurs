"""Defines URL patterns for users"""

from django.urls import path, include

app_name = 'users'
urlpatterns = [
    # Schließt Standard-Authentifizierungs-URLs ein.
    path('', include('django.contrib.auth.urls')),
]
