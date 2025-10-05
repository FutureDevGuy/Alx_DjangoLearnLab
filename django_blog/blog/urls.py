from django.urls import path
from . import views

urlpatterns = [
    # READ: List all posts (used for the homepage)
    path('', views.post_list, name='post_list'),
    
    # CRUD Operations
    # CREATE: Route for creating a new post
    path('post/new/', views.post_new, name='post_new'),
    
    # UPDATE/DETAIL: Route for viewing and updating a specific post
    path('post/<int:pk>/update/', views.post_update, name='post_update'),
    
    # DELETE: Route for deleting a specific post
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    
    # DETAIL: Optional: Add a route for viewing a single post
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
