from django.db import models
from django.contrib.auth.models import User # nie musze tworzyc klasy korzystam z gotowej



class Test(models.Model):
    title= models.CharField(max_length=200)
    body= models.TextField()

    def __str__(self):
        return f"Post: {self.title}"

class Flashcard(models.Model):
    character = models.CharField(max_length=255)
    meaning = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.character




