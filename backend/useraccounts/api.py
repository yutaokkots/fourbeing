from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from useraccounts.serializers import UserSerializer, LoginSerializer, CreateUserSerializer
from knox.auth import TokenAuthentication


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        print(token)
        print(token[1])
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Login API

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(f'this is the serializer {serializer}')
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        print(f'this is the user {user}')
        token = AuthToken.objects.create(user)
        #datetime_format = token.get_expiry_datetime_format()
        print(token)
        print(token[1])
        #print(datetime_format)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Get User API

class UserAPI(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user