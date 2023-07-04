from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import openai


API_KEY = os.environ.get('OPENAI_API_KEY')

#Content-Type: application/json
# OpenAI key
language_dict = {
    "en":"English", 
    "zh":"Mandarin Chinese", 
    "ko":"Korean", 
    "ja":"Japanese", 
    "th":"Thai", 
    "pt":"Portuguese", 
    "vi":"Vietnamese", 
    "ar":"Standard Arabic", 
    "de":"German", 
    "ru":"Russian", 
    "es":"Spanish", 
    "fr":"French", 
    "it":"Italian", 
    "hi":"Hindi", 
    "uk":"Ukranian",
    "my":"Burmese",
    "bg":"Bulgarian"}


@api_view(http_method_names=["POST"])
def translate(request):
    openai.api_key = API_KEY
   
    prompt = request.data["prompt"]
    lang = request.data["language"]
    language = language_dict[lang]
    print(request.data)
    try:
        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Translate this into {language}:\n\n{prompt}\n\n",
            temperature=0.3,
            max_tokens=2048,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )
        response = {
            "message": "success",
            "text": res["choices"][0]["text"]
            }
        
        return Response(data=response, status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(data=exception.args, status=status.HTTP_400_BAD_REQUEST)