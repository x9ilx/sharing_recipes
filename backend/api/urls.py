from django.urls import include, path
from rest_framework import routers

app_name = 'api'

urlpatterns = [
    path('', include('user.urls')),
]
