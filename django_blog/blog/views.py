from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse  # reverse is needed for comment redirects
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View  # Needed for CommentCreateView POST handling
)
from django.db.models import Q  # ✅ Added for search queries

# Import all required items from models and forms
from .models import Post, Comment
from .forms import CustomUserCreationForm, PostForm, CommentForm


# -------------------------------------
# AUTHENTICATION VIEWS (Function-Based)
# -------------------------------------

def register_view(request):
    """Handles user registration and automatic login."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


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

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Includes the comment form in the detail view context."""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# -------------------------------------
# COMMENT CRUD VIEWS
# -------------------------------------

class CommentCreateView(LoginRequiredMixin, View):
    """Handles POST requests to create a new comment via the post detail page."""
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

        return redirect('post_detail', pk=post.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    context_object_name = 'comment'

    def get_success_url(self):
        comment = self.get_object()
        return reverse('post_detail', kwargs={'pk': comment.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        comment = self.get_object()
        return reverse('post_detail', kwargs={'pk': comment.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# -------------------------------------
# SEARCH & TAG FILTER VIEWS
# -------------------------------------

class SearchResultsView(ListView):
    """Displays search results filtered by query across title, content, and tags."""
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-published_date']

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()
        return Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()


class PostsByTagView(ListView):
    """Displays posts filtered by a specific tag."""
    model = Post
    template_name = 'blog/post_list_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-published_date']

    def get_queryset(self):
        tag = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag_name'] = self.kwargs.get('tag_name')
        return ctx
