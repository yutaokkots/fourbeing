import uuid
import boto3
import os

from django.shortcuts import render, redirect
from useraccounts.models import Profile, Photo
from fourbeing.models import Post, Reply
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from useraccounts.serializers import ProfileSerializer, PhotoSerializer
from fourbeing.serializers import PostSerializer, ReplySerializer
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser

# user/profile/<int:user_id>/
@api_view(http_method_names=["GET"])  
def getProfile(request, user_id):
    try:
        profile = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile)
        response = {
            "message": "Profile details",
            "profile": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        response = {
            "message": "No profile exists",
            "profile": "None"
        }
        return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
def createProfile(request, user_id):
    data = request.data
    # user = User.objects.get(id=user_id)
    data['user'] = user_id  # change 'user_id' to 'user'
    serializer = ProfileSerializer(data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response = {
        "message": "Profile created",
        "data": serializer.data
    }
    return Response(data=response, status=status.HTTP_201_CREATED)

@api_view(http_method_names=["PUT"])
def editProfile(request, user_id):
    data = request.data
    print(data)     ##
    print(user_id)  ##
    try:
        profile = Profile.objects.get(pk=user_id)
        print(profile)  ##
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        serializer = ProfileSerializer(profile, data=data, partial=True)
        print("hello")  ##
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)  ##
            print("did it not work?")   ##
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("goodbye")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# api/auth/user/profile/<int:user_id>/get_photo/
@api_view(http_method_names=["GET"])
def get_photo(request, user_id):
    try:
        photo = Photo.objects.get(user_id=user_id)
        serializer = PhotoSerializer(photo)
        response = {
            "message": "Profile details",
            "photo": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    except Photo.DoesNotExist:
        response = {
            "message": "No profile photo exists",
            "photo": "None"
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# api/auth/user/profile/<int:user_id>/add_photo/
@api_view(http_method_names=["POST"])
def add_photo(request, user_id):
    image_file = request.FILES.get('imgfile', None)
    if image_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 
        key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(image_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            photo = Photo.objects.create(url=url, user_id=user_id)
            serializer = PhotoSerializer(photo)
            response = {
                "message": "Profile details",
                "photo": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        

# api/auth/user/profile/<int:user_id>/edit_photo/
@api_view(http_method_names=["PUT"])
def edit_photo(request, user_id):
    image_file = request.FILES.get('imgfile', None)
    if image_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 
        key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(image_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.filter(user_id=user_id).update(url=url)
            photo = Photo.objects.get(user_id=user_id)
            serializer = PhotoSerializer(photo)
            response = {
                "message": "Profile details",
                "photo": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
# api/auth/user/profile/<int:user_id>/get_all_posts/
@api_view(http_method_names=["GET"])
def get_all_posts(request, user_id:int):
    all_user_posts = Post.objects.filter(profile=user_id)
    serializer = PostSerializer(instance=all_user_posts, many=True, partial=True)
    response = { 
        "message": "posts", 
        "data": serializer.data,
    }
    return Response(data=response, status=status.HTTP_200_OK)

# api/auth/user/profile/<int:user_id>/get_all_replies/
@api_view(http_method_names=["GET"])
def get_all_replies(request, user_id:int):
    print("here")
    all_user_replies = Reply.objects.filter(user=user_id)
    serializer = ReplySerializer(instance=all_user_replies, many=True, partial=True)
    response = { 
        "message": "posts", 
        "data": serializer.data,
    }
    print(response)
    return Response(data=response, status=status.HTTP_200_OK)
