from django.urls import path
from . import views
from .views import (
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
)

urlpatterns = [
    # READ: List all posts (homepage)
    path('', views.PostListView.as_view(), name='post_list'),
    
    # CREATE: Route for creating a new post
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    
    # UPDATE: Route for updating a specific post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    
    # DELETE: Route for deleting a specific post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # DETAIL: Route for viewing a single post
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Comment URLs
    path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
