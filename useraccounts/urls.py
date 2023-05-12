from django.urls import path, include
# from knox import views as knox_views
from useraccounts.api import LoginAPI, RegisterAPI, UserAPI  # BaseUserCreationForm #, ManageUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from useraccounts.views import getProfile, createProfile, editProfile

from useraccounts.tokens import MyTokenObtainPairView

# api/auth/

urlpatterns = [

    path('createuser/', RegisterAPI.as_view(), name="createuser"),

    #path('signin/', LoginAPI.as_view(), name='login'),
    path('user/', UserAPI.as_view(), name='user'),
    path('user/profile/<int:user_id>/', getProfile, name="getProfile" ),
    path('user/profile/<int:user_id>/create/', createProfile, name="createProfile" ),
    path('user/profile/<int:user_id>/edit/', editProfile, name="editProfile" ),

    path('signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


]