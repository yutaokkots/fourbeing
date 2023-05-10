from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model


#create user Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


#register Serializer


# class CreateUserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[
#             UniqueValidator(queryset=get_user_model().objects.all())
#         ]
#     )
#     #user object serializer
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#             'password')
#         extra_kwargs = {'password': {'write_only': True, 'min_length':4}}

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')
        extra_kwargs = {'password':{'write_only': True, 'min_length':4}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['email'], validated_data['password'], )
        return user

# class CreateUserSerializer(generics.CreateAPIView):
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token = AuthToken.objects.create(user)
#         print(token)
#         return Response({
#             "users": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": token
#             # "exp:": 
#         })

# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['password'])

#         return user
    
#login Serializer

#login serializer

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self,data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credentials are incorrect")
    
 