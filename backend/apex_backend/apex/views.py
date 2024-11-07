from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Flashcard
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json

def home(request):
    return HttpResponse("hello world")
@api_view(['POST'])
def register(request):
    data= json.loads(request.body)
    username= data.get("username")
    password= data.get("password")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "That user already exists"}, status= 400)
    else:
        user= User.objects.create_user(username=username, password= password)
        return JsonResponse({"message": "User created successfully"}, status= 201)

    print(username, password)
    
   
    #user = User.objects.create_user(username='username', password='haslo123')
    #user.save()


@api_view(['POST'])
def login(request):
     
     data= json.loads(request.body)
     username= data.get("username")
     password= data.get("password")
     print(username, password)
     
     user= authenticate(username= username, password= password)
    
     if user:
         return JsonResponse({"message": user.id}, status= 201)
     else:
         return JsonResponse({"error": "wrong credentials"}, status= 400)
         
    
   

   
@api_view(['POST'])
def flashcards(request):
     print(request)
     data= json.loads(request.body)
     user_id= data.get("user_id")
     flashcards = Flashcard.objects.filter(user_id= user_id)
     print(flashcards)
     flashcards_data = [
        {
            'character': flashcard.character,
            'meaning': flashcard.meaning,
        }
        for flashcard in flashcards
    ]
     if flashcards:
         return JsonResponse({"message":flashcards_data}, status= 201)

    
    

    

@api_view(['GET'])
def getData(request):
    person = {'name': 'Jan', 'age':23}
    return Response(person)


