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
    serializer = PostSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    #print(serializer.data)
    if serializer.is_valid():
        try:
            reply = serializer.save()
            response_data = ReplySerializer(reply).data
            
            response = {
                "message": "Post created",
                "data": response_data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response(data=exception.args, status=status.HTTP_400_BAD_REQUEST)
            
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

def test(request):
    data = Test.objects.all()
    serializer = TestSerializer(data, many=True)
    return JsonResponse({'test': serializer.data})

# gets all of the replies in the fourbeing page
# api/fourbeing/<post_id>/comments/<reply_id>/
@api_view(http_method_names=["GET"])
def reply_index(request):
    all_posts = Reply.objects.all()
    if request.method == "GET":
        serializer = ReplySerializer(instance=all_posts, many=True, partial=True )

        print(serializer.data)
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
    # post = Post.objects.get(id=post_id)
    # print(post)
    # data["post"] = post.id
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
# /api/fourbeing/<post_id>/comments/create/
# api/fourbeing/<post_id>/comments/<reply_id>/create/ 
@api_view(http_method_names=["PUT", "DELETE"])            
def reply_update(request, post_id:int):
    post = get_object_or_404(Post, id=post_id)
    data = request.data
    if request.method == "PUT":
        serializer = PostSerializer(instance=post, data=data, partial=True)
        print(serializer)
        print(serializer.is_valid)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
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


@api_view(http_method_names=["PUT"])
def reply_like(request, reply_id:int):
    reply = Reply.objects.get(pk=reply_id)
    reply.increment_love()