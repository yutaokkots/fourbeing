from fourbeing.models import Test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from fourbeing.serializers import TestSerializer, PostSerializer, UserSerializer, AuthSerializer #from 'serializers.py' file
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from fourbeing.models import Post

posts = [
    {
        "id":1,
        "title":"What is the best way to learn programming?",
        "description": "I am starting a coding bootcamp this year",
    },
]

# gets all of the posts in the fourbeing page
# api/e/fourbeing/
@api_view(http_method_names=["GET"])
def fourbeing_index(request):
    serializer_class = PostSerializer 

    try:
        all_posts = Post.objects.all()
        serializer = PostSerializer(instance=all_posts, many=True)
        print(serializer)
        print(serializer.data)
        response = {
            "message": "posts",
            "data": serializer.data,
        }
        return Response(data=response.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data=e.args, status=status.HTTP_400_BAD_REQUEST)


# allows the creation of new posts
# api/e/fourbeing/create/
@api_view(http_method_names=["POST"])
def createpost(request):
    if request.method == "POST":
        data = request.data
        serializer = PostSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Post created",
                    "data": serializer.data
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response(data=exception.args, status=status.HTTP_400_BAD_REQUEST)
            




@api_view(http_method_names=["GET", "POST"])
def homepage(request):
    if request.method == "POST":
        data = request.data
        response = {"message": "Hello World", "data": data}

        return Response(data=response, status=status.HTTP_201_CREATED)
    response = {"message": "Hello World"}
    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["POST"])
def post_detail(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostSerializer(instance=post)
    response = {
        "message":"post",
        "data":serializer.data
    }
    
    return Response(data=response, status=status.HTTP_200_OK)
    return Response(data={"error": "Post not found"}, status=status.HTTP_200_OK)


@api_view(http_method_names=["PUT"])
def post_update(request, post_id: int):
    # post = get_object_or_404(Post, pk=post_id)

    # if post:
    #     return Response(data=post, status=status.HTTP_200_OK)
    
    # return Response(data={"error": "Post not found"}, status=status.HTTP_200_OK)
    pass

@api_view(http_method_names=["DELETE"])
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