from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
def home(request):
    return HttpResponse("hello world")

def register(request):
    return HttpResponse("register")

def login(request):
    return HttpResponse("login")

def flashcards(request):
    return HttpResponse("flashcards")

@api_view(['GET'])
def getData(request):
    person = {'name': 'Jan', 'age':23}
    return Response(person)


