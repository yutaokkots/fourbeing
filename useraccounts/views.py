import uuid
import boto3
import os

from django.shortcuts import render, redirect
from useraccounts.models import Profile, Photo
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from useraccounts.serializers import ProfileSerializer
from django.contrib.auth.models import User


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
    serializer = ProfileSerializer(data=data)
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
    print(data)
    print(user_id)
    try:
        profile = Profile.objects.get(pk=user_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        serializer = ProfileSerializer(profile, data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# user/profile/<int:user_id>/add_photo/
@api_view(http_method_names=["POST"])
def add_photo(request, cat_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    #return redirect('detail', cat_id=cat_id)