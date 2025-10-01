# api/views.py
from rest_framework import generics, viewsets
from .serializers import BookSerializer
from .models import Book

# Note: Keep the BookList view from the previous task for now, 
# as the instructions ask to keep its URL.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# New: ViewSet for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet that provides list, retrieve, create, update, and destroy actions 
    for the Book model.
    """
    # Required for listing and retrieving
    queryset = Book.objects.all()
    
    # Required for creating, updating, and serializing
    serializer_class = BookSerializer