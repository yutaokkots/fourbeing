from django.urls import path, include
from knox import views as knox_views
from useraccounts.api import LoginAPI, RegisterAPI, UserAPI #, ManageUserView


urlpatterns = [

    path('createuser/', RegisterAPI.as_view(), name="createuser"),
    path('signin/', LoginAPI.as_view(), name='knox_login'),
    path('user/', UserAPI.as_view(), name='user'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),

    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('', include('knox.urls')),
]