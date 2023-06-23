import uuid
import boto3
import os
import json
import base64


from fourbeing.models import Test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from fourbeing.serializers import TestSerializer, PostSerializer, ReplySerializer, AuthSerializer #from 'serializers.py' file
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from fourbeing.models import Post, Reply
from django.contrib.auth.models import User


# gets all of the posts in the fourbeing page
# api/fourbeing/
@api_view(http_method_names=["GET"])
def index(request):
    all_posts = Post.objects.all()
    if request.method == "GET":
        serializer = PostSerializer(instance=all_posts, many=True, partial=True )
        response = { 
            "message": "posts", 
            "data": serializer.data,
        }
        return Response(data=response, status=status.HTTP_200_OK)

# allows the creation of new posts
# api/fourbeing/create/
@api_view(http_method_names=["POST"])
def createpost(request):
    data = request.data
    username = (data["username"])
    user = User.objects.get(username = username)
    data["profile"] = user.id
    print(data)
    serializer = PostSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    #print(serializer.data)
    if serializer.is_valid():
        try:
            serializer.save()
            #response_data = ReplySerializer(reply).data
            
            response = {
                "message": "Post created",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response(data=exception.args, status=status.HTTP_400_BAD_REQUEST)
        
# allows the creation of new posts
# api/fourbeing/createPhoto/
@api_view(http_method_names=["POST"])
def createpostphoto(request):
    image_file = request.FILES.get('imgfile', None)
    if image_file:
        data_json = request.POST.get("postdata", None)
        if data_json:
            data = json.loads(data_json)
            username = (data["username"])
            user = User.objects.get(username = username)
            data["profile"] = user.id
            s3 = boto3.client('s3')
            # need a unique "key" for S3 
            key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(image_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                data["photo"] = url
                serializer = PostSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    response = {
                        "message": "Profile details",
                        "photo": serializer.data
                    }
                    return Response(data=response, status=status.HTTP_200_OK)
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    # username = (data["username"])
    # description = (data["description"])
    # print(username)
    # print(description)
    # user = User.objects.get(username = username)
    # data["profile"] = user.id
    # print(data)
    # serializer = PostSerializer(data=data)
    # serializer.is_valid(raise_exception=True)
    # #print(serializer.data)
    # if serializer.is_valid():
    #     try:
    #         serializer.save()
    #         #response_data = ReplySerializer(reply).data
            
    #         response = {
    #             "message": "Post created",
    #             "data": serializer.data
    #         }
    #         return Response(data=response, status=status.HTTP_201_CREATED)
    #     except Exception as exception:
    #         return Response(data=exception.args, status=status.HTTP_400_BAD_REQUEST)
            


# allows the retrieval of a single post, returns the profile name as well
# api/fourbeing/<post_id>/
@api_view(http_method_names=["GET"])
def post_detail(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostSerializer(instance=post)
    profile_id = serializer.data["profile"]
    user = User.objects.get(id=profile_id)
    serializer.data["username"] = user
    response = {
        "message":"post",
        "data":serializer.data
    }    
    return Response(data=response, status=status.HTTP_200_OK)

# allows the update or deletion of a post
# api/fourbeing/<post_id>/update or api/fourbeing/<post_id>/update
@api_view(http_method_names=["PUT", "DELETE"])            
def post_update(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    data = request.data
    if request.method == "PUT":
        serializer = PostSerializer(instance=post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
def post_delete(request, post_id: int):
    # post = get_object_or_404(Post, pk=post_id)

    # if post:
    #     return Response(data=post, status=status.HTTP_200_OK)
    
    # return Response(data={"error": "Post not found"}, status=status.HTTP_200_OK)
    pass

# allows the update of the number of loves a comment gets
# api/fourbeing/<post_id>/love/ 
@api_view(http_method_names=["PUT"])
def post_love(request, post_id: int):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    response = {
            "message": "Love added",
            "data": "Thank you BTY!"
        }
    if post.username == "[deleted]":
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        post.add_love()
        return Response(data=response, status=status.HTTP_200_OK)

def test(request):
    data = Test.objects.all()
    serializer = TestSerializer(data, many=True)
    return JsonResponse({'test': serializer.data})

# gets all of the replies in the fourbeing page
# api/fourbeing/<post_id>/comments/<reply_id>/
@api_view(http_method_names=["GET"])
def reply_index(request, post_id):
    #all_posts = Reply.objects.all()
    all_posts = Reply.objects.filter(post=post_id)
    if request.method == "GET":
        serializer = ReplySerializer(instance=all_posts, many=True, partial=True )

        response = { 
            "message": "posts", 
            "data": serializer.data,
        }
        return Response(data=response, status=status.HTTP_200_OK)
    
# allows the creation of new replies
# api/fourbeing/<post_id>/comments/<reply_id>/reply_create/
@api_view(http_method_names=["POST"])
def reply_create(request, post_id:int):
    data = request.data
    print(data["post"])
    serializer = ReplySerializer(data=data)
    
    serializer.is_valid(raise_exception=True)
    print(serializer.errors)
    if serializer.is_valid():
        try:
            #print(serializer.validate_post(data["post"]))
            serializer.save() 
            
            response = {
                "message": "Post created",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response(data=exception.args, status=status.HTTP_400_BAD_REQUEST)

# allows the update and deletion of replies
# api/fourbeing/<post_id>/comments/<reply_id>/create/ 
@api_view(http_method_names=["PUT", "DELETE"])            
def reply_update(request, post_id:int, reply_id:int):
    data = request.data
    try:
        reply= Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        serializer = ReplySerializer(reply, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# allows the update of the number of loves a comment gets
# api/fourbeing/<post_id>/comments/<reply_id>/love/ 
@api_view(http_method_names=["PUT"])
def reply_love(request, post_id:int, reply_id:int):
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    response = {
            "message": "Love added",
            "data": "Things are great, either way"
        }
    if reply.username == "[deleted]":
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        reply.add_love()
        return Response(data=response, status=status.HTTP_200_OK)

