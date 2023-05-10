from django.urls import path, include
# from knox import views as knox_views
from useraccounts.api import LoginAPI, RegisterAPI, UserAPI #, ManageUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from useraccounts.tokens import MyTokenObtainPairView

urlpatterns = [

    path('createuser/', RegisterAPI.as_view(), name="createuser"),
    #path('signin/', LoginAPI.as_view(), name='login'),
    path('user/', UserAPI.as_view(), name='user'),
    # path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),

    #django-rest-framework jwt token routes
    #/api/auth/token
    path('signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    #path('', include('knox.urls')),
]