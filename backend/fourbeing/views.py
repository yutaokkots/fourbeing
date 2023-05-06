from django.shortcuts import render
from fourbeing.models import Test
from django.http import JsonResponse
from fourbeing.serializers import TestSerializer


#invoke serializer that converts db object to the json data and return to client. 

def test(request):
    data = Test.objects.all()
    serializer = TestSerializer(data, many=True)
    return JsonResponse({'test': serializer.data})
    pass

