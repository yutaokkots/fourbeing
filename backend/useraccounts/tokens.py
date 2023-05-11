from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

def create_jwt_pair_for_user(user:User):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access" : str(refresh.access_token),
        "refresh": str(refresh)
    }

    return tokens

## create a custom token that includes userinfo
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom field; username to the token
        token['name'] = user.username
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

