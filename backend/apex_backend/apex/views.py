from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from apex.serializers.flashcard_serializer import FlashcardSerializer
from apex.models import Flashcard, Pupil
from apex.scripts.super_memo import super_memo
from django.utils.timezone import now
from datetime import timedelta

def home(request):
    return HttpResponse("hello world")

@api_view(['POST'])
def update_flashcards(request):
    data= json.loads(request.body)
    flashcard_id= data.get("id")
    user_grade= data.get("user_answer") 
    pupil_dilatation= data.get("pupil_dilatation")

    flashcard= Flashcard.objects.get(id= flashcard_id)
    if not flashcard:
        return JsonResponse(
            {"error":"Nie znaleziony fiszki z takim id"}, status= 400
        )
    serializer= FlashcardSerializer(flashcard)
    repetition_number= serializer.data.get("repetition_number")
    ef= serializer.data.get("easiness_factor")
    interval= serializer.data.get("interval")
    #pupil_dilatation= serializer.data.get("pupil_dilatation")
    print(flashcard_id, user_grade, pupil_dilatation, repetition_number, ef, interval)

    new_repetition_number, new_ef, new_interval= super_memo(user_grade, repetition_number, ef, interval, pupil_dilatation)

    flashcard.repetition_number= new_repetition_number
    flashcard.easiness_factor= new_ef
    flashcard.last_repetition_date = now().date()
    flashcard.next_repetition_date= now().date() + timedelta(days= new_interval)
    flashcard.save()

    pupil= Pupil.objects.create(
        flashcard= flashcard,
        dilatation= pupil_dilatation,
        timestamp1= now().date() + timedelta(days= 0)
    )
    pupil.save()
    
    return JsonResponse(
        {"message":"zaktualizowalem dane"}, status= 200
        )


@api_view(['GET', 'POST'])
def flashcards(request):
    data= json.loads(request.body)
    user_id= data.get("user_id")
    print(now().date())
    flashcards = Flashcard.objects.filter(user_id=user_id, next_repetition_date__lte=now().date())
    print(flashcards)

    if flashcards:
        serializer= FlashcardSerializer(flashcards, many= True)
        return JsonResponse(
            {"flashcards" : serializer.data}, status= 200
        )
    else:
        return JsonResponse(
            {"error":"This user has no flashcards"}, status= 400
        )



@api_view(['POST', 'GET'])
def register(request):
    data = json.loads(request.body)
    email= data.get("email")
    password= data.get("password")

    if User.objects.filter(email=email):
        return JsonResponse(
            {"error": "user z takim email juz istnieje"}
        )
    else:
         user = User.objects.create_user(username= email, email=email, password=password)
         return JsonResponse(
             {"message":"sukcces, utworzono uzytkownika"}, status= 201
         )


     
    
@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    email= data.get("email")
    password= data.get("password")
    user= authenticate(username= email, email= email, password= password)

    if user is not None:
        return JsonResponse(
            {"message": "zalogowano pomyslnie", "user_id": user.id}, status=200
        )
    else:
         return JsonResponse(
            {"error": "nieprawidlowe dane"}, status=400
        )
        

  

    



