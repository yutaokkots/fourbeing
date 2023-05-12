from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from useraccounts.models import Profile

#create user Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    passwordConfirm = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'passwordConfirm')
        extra_kwargs = {'password':{'write_only': True, 'min_length':4}}

    def validate(self, attrs):
        if attrs['password'] != attrs['passwordConfirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'], 
            validated_data['password'], )
        return user 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self,data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credentials are incorrect")
 
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['title', 'bio', 'location', 'website']
#     def create(self, validated_data):
#         print(validated_data)
#         user = validated_data.user
#         profile = Profile.objects.create(user=user, **validated_data)
#         return profile
    
    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    #     student, created = Profile.objects.update_or_create(user=user,
    #         title=validated_data.pop('title'),
    #         bio=validated_data.pop('bio'),
    #         location=validated_data.pop('location'),
    #         website=validated_data.pop('website')
    #         )
    #     return student

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['user','title', 'bio', 'location', 'website']

#     def create(self, validated_data):
#         #user_id = validated_data.pop('user')
#         print(validated_data)
#         user = User.objects.get(username=validated_data['user'])
#         profile = Profile.objects.create(
#             user=user
#             validated_data['title'], 
#             validated_data['bio'],
#             validated_data['location'],
#             validated_data['website'],
#             )
#         return profile
    


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','title', 'bio', 'location', 'website']

    def create(self, validated_data):
        username = validated_data['user']
        user = User.objects.get(username=username)
        profile = Profile.objects.create(
            user=user,
            title=validated_data['title'], 
            bio=validated_data['bio'],
            location=validated_data['location'],
            website=validated_data['website'],
        )
        return profile