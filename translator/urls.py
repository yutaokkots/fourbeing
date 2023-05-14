from django.urls import path, include
from . import views

# import routers
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    path('', views.translate, name="translate" ),
]