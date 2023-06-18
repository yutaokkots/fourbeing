from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.serializers import DateTimeField
#from knox.models import AuthToken
from useraccounts.serializers import UserSerializer, UsernameSerializer, ProfileSerializer, LoginSerializer, CreateUserSerializer

from django.utils import timezone
#from knox.auth import TokenAuthentication
#from knox.settings import knox_settings, CONSTANTS
#from knox.views import LoginView as KnoxLoginView

from rest_framework import status
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import authenticate, password_validation
from fourbeing.models import User
from useraccounts.models import Profile
from useraccounts.tokens import create_jwt_pair_for_user, MyTokenObtainPairSerializer, MyTokenObtainPairView
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json

# Register API -> registers user, generates token, and returns 
class RegisterAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user_instance = serializer.save()
            user_id = user_instance.id
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)
            profile = Profile.objects.filter(user_id=user_id).first()
            if profile:
                profile.username = username
                profile.title = "New user!"
                profile.save()
            print(profile)
            response = {
                "message":"user created successfully",
                "token": "getToken"
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    # post request. (1) retrieves 'username' + 'password' from request, (2) serializes data and checks,
    # (3) if user is found, then create a new access token and returns user info + token
    def post(self, request,  *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]
        serializer = MyTokenObtainPairSerializer(data=request.data)
        user = authenticate(username=username, password=password)
        serializer.is_valid(raise_exception=True)
        if user is not None:
            token = create_jwt_pair_for_user(user)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token,
            })
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPI(generics.RetrieveAPIView):
    authentication_classes = ()
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user