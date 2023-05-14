from rest_framework import serializers
from fourbeing.models import Test, Post, Reply

# serializer for create_user request
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, get_user_model

from rest_framework.validators import UniqueValidator

from rest_framework.response import Response
# from knox.auth import AuthToken
from django.shortcuts import get_object_or_404

class PostSerializer(serializers.ModelSerializer):
    #replies = serializers.RelatedField(many=True, read_only=True) # related field to Reply model
    class Meta:
        model = Post
        fields = ['id','title', 'description', 'created', 'profile', "username", "love"]
        # extra_kwargs = {
        #     'title': {'required': True},
        #     'description': {'required': True},
        # }


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('name', 'description')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=get_user_model().objects.all())
        ]
    )
    #user object serializer
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length':4}}


    
class AuthSerializer(serializers.Serializer):
    #user authentication object serializer
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": 'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user =  authenticate(
            request = self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            message = ('Unable to authenticate user')
            raise serializers.ValidationError(message, code='authentication')
        
        attrs['user'] = user
        return 

class ReplySerializer(serializers.ModelSerializer):
    # comment = serializers.CharField()
    # username = serializers.CharField()

    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    # post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)
    class Meta:
        model = Reply
        fields = ['comment', 'username', 'user', 'post', 'created', 'love', 'id']
    

    # def validate_post(self, value):
    #     post_id = value
    #     post = get_object_or_404(Post, id=post_id)
    #     return post
    #     # if not isinstance(value, Post):
    #     #     raise serializers.ValidationError("Invalid Post")
    #     # return value

    # def create(self, validated_data):
    #     reply = Reply.objects.create(**validated_data)
    #     return reply
    

    
    # def create(self, validated_data):
    #     reply = Reply.objects.create(
    #         post = validated_data['post'],
    #         username = validated_data['username'],
    #         user = validated_data['user'],
    #         comment = validated_data['comment']
    #     )
    #     reply.save()
     #   return reply
    
