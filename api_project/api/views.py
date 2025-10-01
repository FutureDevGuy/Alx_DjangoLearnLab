# api/views.py
from rest_framework import generics
# Import the serializer we just created
from .serializers import BookSerializer
# Import the model
from .models import Book

class BookList(generics.ListAPIView):
    # 1. Define the queryset: what data should this view retrieve?
    # We want all Book objects.
    queryset = Book.objects.all()
    
    # 2. Define the serializer_class: how should the data be formatted?
    # We use the BookSerializer we defined.
    serializer_class = BookSerializer