from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse # reverse is needed for comment redirects
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    View # Needed for CommentCreateView POST handling
)

# Import all required items from models and forms
from .models import Post, Comment 
from .forms import CustomUserCreationForm, PostForm, CommentForm 


# -------------------------------------
# AUTHENTICATION VIEWS (Function-Based)
# -------------------------------------

# Registration view
def register_view(request):
    """Handles user registration and automatic login."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            # NOTE: Redirecting to 'profile' requires you define a 'profile' URL name.
            return redirect('profile') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Login view
def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            # NOTE: Redirecting to 'profile' requires you define a 'profile' URL name.
            return redirect('profile') 
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# Logout view
def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.success(request, "Logged out successfully.")
    # NOTE: Redirecting to 'login' requires you define a 'login' URL name.
    return redirect('login') 

# Profile view
@login_required
def profile_view(request):
    """Displays user profile (requires login)."""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated successfully.")
    return render(request, 'blog/profile.html')


# -------------------------------------
# BLOG POST CRUD VIEWS (Class-Based)
# -------------------------------------

# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html' # Changed from post_list.html for consistency with initial setup
    context_object_name = 'posts'
    ordering = ['-published_date'] 

# Show details of a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Includes the comment form in the detail view context."""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm() 
        return context

# Create a new post (Requires login)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm # Use the form_class from forms.py
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list') # Redirect to the post list after creation

    def form_valid(self, form):
        """Sets the author field to the logged-in user."""
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a post (Requires login and authorship)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm # Use the form_class from forms.py
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        """Sets the author field to the logged-in user."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Checks if the logged-in user is the post author."""
        post = self.get_object()
        return self.request.user == post.author

# Delete a post (Requires login and authorship)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list') # Redirect to the post list after deletion

    def test_func(self):
        """Checks if the logged-in user is the post author."""
        post = self.get_object()
        return self.request.user == post.author


# -------------------------------------
# COMMENT CRUD VIEWS
# -------------------------------------

class CommentCreateView(LoginRequiredMixin, View):
    """
    Handles POST requests to create a new comment via the post detail page.
    Uses View instead of CreateView for simpler redirect logic.
    """
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        
        # Always redirect back to the post detail page
        return redirect('post_detail', pk=post.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows the comment author to edit their comment.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' 
    context_object_name = 'comment'

    def get_success_url(self):
        """Redirects back to the parent post's detail page after update."""
        comment = self.get_object()
        return reverse('post_detail', kwargs={'pk': comment.post.pk})

    def test_func(self):
        """Checks if the logged-in user is the comment author."""
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the comment author to delete their comment.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html' 
    context_object_name = 'comment'

    def get_success_url(self):
        """Redirects back to the parent post's detail page after deletion."""
        comment = self.get_object()
        return reverse('post_detail', kwargs={'pk': comment.post.pk})

    def test_func(self):
        """Checks if the logged-in user is the comment author."""
        comment = self.get_object()
        return self.request.user == comment.author
