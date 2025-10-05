from django.urls import path
from . import views

urlpatterns = [
    # -------------------------------------
    # BLOG POST CRUD URLs
    # -------------------------------------
    
    # READ: List all posts (homepage)
    path('', views.PostListView.as_view(), name='post_list'),
    
    # CREATE: Route for creating a new post
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    
    # DETAIL: Route for viewing a single post
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # UPDATE: Route for updating a specific post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    
    # DELETE: Route for deleting a specific post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # -------------------------------------
    # USER AUTHENTICATION URLs
    # -------------------------------------
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # -------------------------------------
    # COMMENT CRUD URLs (Updated to match requested structure)
    # -------------------------------------
    
    # CREATE: Create a comment on a specific post
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    
    # UPDATE: Edit a specific comment
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    
    # DELETE: Delete a specific comment
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
