from django.urls import path, include
# from knox import views as knox_views
from useraccounts.api import LoginAPI, RegisterAPI, UserAPI # BaseUserCreationForm #, ManageUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from useraccounts.views import getProfile, createProfile, editProfile, add_photo, get_photo, edit_photo
from useraccounts.tokens import MyTokenObtainPairView

# api/auth/

urlpatterns = [

    path('createuser/', RegisterAPI.as_view(), name="createuser"),

    #path('signin/', LoginAPI.as_view(), name='login'),
    path('user/', UserAPI.as_view(), name='user'),
    path('user/profile/<int:user_id>/', getProfile, name="getProfile" ),
    path('user/profile/<int:user_id>/create/', createProfile, name="createProfile" ),
    path('user/profile/<int:user_id>/edit/', editProfile, name="editProfile" ),
    path('user/profile/<int:user_id>/get_photo/', get_photo, name='get_photo'),
    path('user/profile/<int:user_id>/add_photo/', add_photo, name='add_photo'),
    path('user/profile/<int:user_id>/edit_photo/', edit_photo, name='edit_photo'),
    path('signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]