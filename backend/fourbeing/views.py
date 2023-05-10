from fourbeing.models import Test
from django.http import JsonResponse
from fourbeing.serializers import TestSerializer, UserSerializer, AuthSerializer #from 'serializers.py' file
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from fourbeing.models import Post
from fourbeing.serializers import PostSerializer

posts = [
    {
        "id":1,
        "title":"What is the best way to learn programming?",
        "description": "I am starting a coding bootcamp this uear",
    },
]

# gets all of the posts in the fourbeing page
# api/e/fourbeing/
@api_view(http_method_names=["GET"])
def fourbeing_index(request: Request):
    
    try:
        all_posts = Post.objects.all()
        serializer = PostSerializer(instance=all_posts, many=True)
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
def createpost(request: Request):
    if request.method == "POST":
        data = request.data
        serializer = PostSerializer(data=data)
        try:
            serializer.save()
            response = {
                "message": "Post created",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response(data=exception.args, status=status.HTTP_400_BAD_REQUEST)
            




@api_view(http_method_names=["GET", "POST"])
def homepage(request:Request):
    if request.method == "POST":
        data = request.data
        response = {"message": "Hello World", "data": data}

        return Response(data=response, status=status.HTTP_201_CREATED)
    response = {"message": "Hello World"}
    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["GET"])
def post_detail(request: Request, post_index: int):
    post = posts[post_index]

    if post:
        return Response(data=post, status=status.HTTP_200_OK)
    
    return Response(data={"error": "Post not found"}, status=status.HTTP_200_OK)


def test(request):
    

    data = Test.objects.all()
    serializer = TestSerializer(data, many=True)
    return JsonResponse({'test': serializer.data})