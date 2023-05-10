from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.serializers import DateTimeField
from knox.models import AuthToken
from useraccounts.serializers import UserSerializer, LoginSerializer, CreateUserSerializer

from django.utils import timezone
from knox.auth import TokenAuthentication
from knox.settings import knox_settings, CONSTANTS
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from django.contrib.auth.signals import user_logged_in, user_logged_out
from fourbeing.models import User


import json

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message":"user created successfully",
                "data":serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        ## create a Profile alongisde User here
        print(token)
        print(token[1])
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


#Login API

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
   
    # def get_post_response_data(self, request, token, instance):
    # #     UserSerializer = self.get_user_serializer_class()

    def post(self, request,  *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)

        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data


        #user = authenticate(username=username, password=password)

        print(f'this is the user {user}')
        token = AuthToken.objects.create(user)
        #datetime_format = token.get_expiry_datetime_format()
        #print(datetime_format)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            #"exp": AuthToken.objects.create(expiry)[1],
        })



# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         json_item = json.loads(request.body)
#         username = json_item["username"]
#         print(username)
#         user = User.objects.user(user=username)
#         print(user)
#         # n_context = self.format_expiry_datetime
#         # print(n_context)
#         serializer = AuthToken.objects.filter(user=username)
#         print(serializer)
#         # serializer.is_valid(raise_exception=True)
#         # user = serializer.validated_data['user']
#         # #login(request, user,)[enter image description here][1]
#         # return super(LoginAPI, self).post(request, format=None)
#         return Response({
#             "user": "hello",
#             "token": "123456",
#             #"exp": AuthToken.objects.create(expiry)[1],
#         })



# class LoginAPI(KnoxLoginView):
#     serializer_class = LoginSerializer
#     permission_classes = (permissions.AllowAny,)
#     #permission_classes = (permissions.IsAuthenticated,)

#     def get_context(self):
#         return {'request': self.request, 'format': self.format_kwarg, 'view': self}

#     def get_token_ttl(self):
#         return knox_settings.TOKEN_TTL

#     def get_token_prefix(self):
#         return ""

#     def get_token_limit_per_user(self):
#         return knox_settings.TOKEN_LIMIT_PER_USER

#     def get_user_serializer_class(self):
#         return knox_settings.USER_SERIALIZER

#     def get_expiry_datetime_format(self):
#         return knox_settings.EXPIRY_DATETIME_FORMAT

#     def format_expiry_datetime(self, expiry):
#         datetime_format = self.get_expiry_datetime_format()
#         return DateTimeField(format=datetime_format).to_representation(expiry)

#     def create_token(self):
#         token_prefix = self.get_token_prefix()
#         return AuthToken.objects.create(
#             user=self.request.user, expiry=self.get_token_ttl()
#         )

#     def get_post_response_data(self, request, token, instance):
#         UserSerializer = self.get_user_serializer_class()

#         data = {
#             'expiry': self.format_expiry_datetime(instance.expiry),
#             'token': token
#         }
#         if UserSerializer is not None:
#             data["user"] = UserSerializer(
#                 request.user,
#                 context=self.get_context()
#             ).data
#         return data

#     def post(self, request, format=None):
#         token_limit_per_user = self.get_token_limit_per_user()
#         if token_limit_per_user is not None:
#             now = timezone.now()
#             token = request.user.auth_token_set.filter(expiry__gt=now)
#             if token.count() >= token_limit_per_user:
#                 return Response(
#                     {"error": "Maximum amount of tokens allowed per user exceeded."},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
#         instance, token = self.create_token()
#         user_logged_in.send(sender=request.user.__class__,
#                             request=request, user=request.user)
#         data = self.get_post_response_data(request, token, instance)
#         print(data)
#         return Response(data)


# Get User API

class UserAPI(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user