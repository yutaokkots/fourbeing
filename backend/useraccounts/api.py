from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.serializers import DateTimeField
#from knox.models import AuthToken
from useraccounts.serializers import UserSerializer, UsernameSerializer, LoginSerializer, CreateUserSerializer

from django.utils import timezone
#from knox.auth import TokenAuthentication
#from knox.settings import knox_settings, CONSTANTS
#from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import authenticate, password_validation
from fourbeing.models import User
from useraccounts.tokens import create_jwt_pair_for_user, MyTokenObtainPairSerializer, MyTokenObtainPairView
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json

# Register API -> registers user, generates token, and returns 
class RegisterAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        #serializer.is_valid(raise_exception=True)
        #print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)
            #serializer = MyTokenObtainPairSerializer(data=request.data)
            #token = create_jwt_pair_for_user(user)
            response = {
                "message":"user created successfully",
                "token": "getToken"
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class BaseUserCreationForm(forms.ModelForm):
#     """
#     A form that creates a user, with no privileges, from the given username and
#     password.
#     """

#     error_messages = {
#         "password_mismatch": _("The two password fields didn’t match."),
#     }
#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#         strip=False,
#         help_text=_("Enter the same password as before, for verification."),
#     )

#     class Meta:
#         model = User
#         fields = ("username",)
#         #field_classes = {"username": UsernameField}

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self._meta.model.USERNAME_FIELD in self.fields:
#             self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
#                 "autofocus"
#             ] = True

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("passwordConfirm")
#         if password1 and password2 and password1 != password2:
#             raise ValidationError(
#                 self.error_messages["password_mismatch"],
#                 code="password_mismatch",
#             )
#         return password2

#     def _post_clean(self):
#         super()._post_clean()
#         # Validate the password after self.instance is updated with form data
#         # by super().
#         password = self.cleaned_data.get("passwordC")
#         if password:
#             try:
#                 password_validation.validate_password(password, self.instance)
#             except ValidationError as error:
#                 self.add_error("password2", error)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#             if hasattr(self, "save_m2m"):
#                 self.save_m2m()
#         return user


#Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    # post request. (1) retrieves 'username' + 'password' from request, (2) serializes data and checks,
    # (3) if user is found, then create a new access token and returns user info + token
    def post(self, request,  *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]
        #serializer = self.get_serializer(data=request.data)
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