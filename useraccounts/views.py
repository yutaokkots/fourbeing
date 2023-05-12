from django.shortcuts import render, redirect
from useraccounts.models import Profile
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

# @api_view(http_method_names=["POST"])
# def createProfile(request, user_id):
#     data = request.data
#     user = User.objects.get(id=user_id)
#     # print(user)
#     # print(user.id)
#     data['user_id'] = user.id
#     # print(data)
#     serializer = ProfileSerializer(data=data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     if serializer.is_valid():
#         try:
#             serializer.create(validated_data=data)
#             serializer.save()
#             response = {
#                 "message": "Profile created",
#                 "data": serializer.data
#             }
#             return Response(data=response, status=status.HTTP_201_CREATED)
#         except Exception as exception:
#             return Response(data=exception.args, status=status.HTTP_400_BAD_REQUEST)

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
    pass 