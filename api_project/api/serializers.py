# api/serializers.py
from rest_framework import serializers
# Assuming your Book model is in api/models.py
from .models import Book 

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        # 1. Specify the model to serialize
        model = Book
        # 2. Specify the fields to include in the output JSON
        # '__all__' is a shortcut for including all fields from the model
        fields = '__all__'