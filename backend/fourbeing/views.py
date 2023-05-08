from django.shortcuts import render
from django.http import JsonResponse
from fourbeing.models import Test
from fourbeing.serializers import TestSerializer, UserSerializer, AuthSerializer #from 'serializers.py' file
from django.utils import timezone
from django.contrib.auth import login

## authentication using rest_framework and knox
from rest_framework import permissions, authentication, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

#from knox.models import get_token_model
from knox.settings import knox_settings

from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.settings import api_settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import status

from rest_framework.response import Response
from knox.auth import AuthToken

# 'generics.CreateAPIView' comes from rest_framework
# class CreateUserView(generics.CreateAPIView):
#     #create user API view
#     serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response({
            "users": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1]
        })



# class LoginView(KnoxLoginView):
#     #login view that extends 'KnoxLoginView'
#     serializer_class = AuthSerializer
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginView, self).post(request, format=None)




class LoginView(KnoxLoginView):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = (permissions.IsAuthenticated,)

    def get_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_token_prefix(self):
        return knox_settings.TOKEN_PREFIX

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_user_serializer_class(self):
        return knox_settings.USER_SERIALIZER

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def create_token(self):
        token_prefix = self.get_token_prefix()
        return TokenAuthentication().objects.create(
            user=self.request.user, expiry=self.get_token_ttl(), prefix=token_prefix
        )

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data

    def post(self, request, format=None):
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        instance, token = self.create_token()
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        return Response(data)



# UserAPIView
class ManageUserView(generics.RetrieveUpdateAPIView):
    #manage the authenticated user
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated)

    def get_object(self):
        #retrieve and reutrn the authenticated user
        return self.request.user



#invoke serializer that converts db object to the json data and return to client. 
# uses 'TestSerializer' class from rest_framework serializer
def test(request):
    data = Test.objects.all()
    serializer = TestSerializer(data, many=True)
    return JsonResponse({'test': serializer.data})