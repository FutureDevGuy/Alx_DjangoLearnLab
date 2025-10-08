from django.urls import path
from . import views
from .views import (
    SearchResultsView,
    PostsByTagView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    # -------------------------------------
    # BLOG POST CRUD URLs
    # -------------------------------------

    # READ: List all posts (homepage)
    path('', PostListView.as_view(), name='post_list'),

    # CREATE: Create a new post
    path('post/new/', PostCreateView.as_view(), name='post_create'),

    # DETAIL: View a single post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # UPDATE: Edit a specific post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),

    # DELETE: Delete a specific post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # -------------------------------------
    # TAGS & SEARCH URLs
    # -------------------------------------

    # SEARCH: Display search results
    path('search/', SearchResultsView.as_view(), name='search'),

    # TAGS: Display posts filtered by a tag
    path('tags/<str:tag_name>/', PostsByTagView.as_view(), name='posts-by-tag'),

    # -------------------------------------
    # COMMENT CRUD URLs
    # -------------------------------------

    # CREATE: Add a new comment to a specific post
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),

    # UPDATE: Edit a specific comment
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),

    # DELETE: Delete a specific comment
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # -------------------------------------
    # USER AUTHENTICATION URLs
    # -------------------------------------

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
