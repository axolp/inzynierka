from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    title= models.CharField(max_length=200)
    body= models.TextField()

    def __str__(self):
        return f"Post: {self.title}"
    
class Flashcard(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE) # django sam dodaje _id
    characters= models.CharField(max_length= 200)
    meaning= models.CharField(max_length=200)
    interval= models.IntegerField(max_length=200, default= 0)
    repetition_number= models.IntegerField(default= 0)
    easiness_factor= models.FloatField(default= 2.5)
    last_repetition_date= models.DateField(default="1969-07-20")
    next_repetition_date= models.DateField(default="1969-07-20")
    pupil_dilatation= models.FloatField(default= 0)

class Pupil(models.Model):
    flashcard= models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    dilatation= models.FloatField(default= 0)
    timestamp1= models.DateField(default="1969-07-20")
    #timestamp1= models.DateField(default="1969-07-20")

    




