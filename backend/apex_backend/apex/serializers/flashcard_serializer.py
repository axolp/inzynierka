from rest_framework import serializers
from apex.models import Flashcard

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'characters', 'meaning', 'repetition_number', 'easiness_factor', 'last_repetition_date', 'next_repetition_date', 'interval']
