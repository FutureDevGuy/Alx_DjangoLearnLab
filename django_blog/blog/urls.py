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
    path('profile/', views.profile_view, name='profile'), # Requires templates/blog/profile.html
    
    # -------------------------------------
    # COMMENT CRUD URLs
    # -------------------------------------
    
    # CREATE: Route for submitting a new comment on a specific post
    # Note: Uses post_id to link to the parent Post
    path('posts/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    
    # UPDATE: Route for editing a specific comment
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    
    # DELETE: Route for deleting a specific comment
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
