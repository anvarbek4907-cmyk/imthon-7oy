from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Post, Category, Comment, Like
from .forms import PostForm, CommentForm


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        posts = Post.objects.filter(status='PUBLISHED')

        search = self.request.GET.get('q', '').strip()

        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(desc__icontains=search) |
                Q(author__username__icontains=search)
            )

        sort = self.request.GET.get('sort', 'new')

        if sort == 'new':
            posts = posts.order_by('-created_at')
        elif sort == 'old':
            posts = posts.order_by('created_at')
        elif sort == 'recent':
            posts = posts.order_by('-updated_at')
        elif sort == 'views':
            posts = posts.order_by('-views_count')
        elif sort == 'likes':
            if self.request.user.is_authenticated:
                posts = posts.filter(
                    likes__user=self.request.user
                ).order_by('-created_at')
            else:
                posts = Post.objects.none()
        else:
            posts = posts.order_by('-created_at')

        return posts


class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs['slug'],
            status='PUBLISHED'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['slug']
        )

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        context['similar_posts'] = Post.objects.filter(
            status='PUBLISHED',
            category=post.category
        ).exclude(
            pk=post.pk
        ).order_by('-created_at')[:3]

        context['recently_posts'] = Post.objects.filter(
            status='PUBLISHED'
        ).exclude(
            pk=post.pk
        ).order_by('-created_at')[:5]

        context['comments'] = post.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        context['like_count'] = post.likes.count()

        if self.request.user.is_authenticated:
            context['user_liked'] = Like.objects.filter(
                post=post,
                user=self.request.user
            ).exists()
        else:
            context['user_liked'] = False

        return context


@login_required
def like_post(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status='PUBLISHED'
    )

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect(
        'post-detail',
        slug=post.slug
    )


class LikedPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/liked_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            likes__user=self.request.user,
            status='PUBLISHED'
        ).order_by('-likes__created_at')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'PUBLISHED'
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        post = self.get_object()

        return (
            self.request.user == post.author
            or self.request.user.is_superuser
        )

    def get_success_url(self):
        return reverse_lazy(
            'post-detail',
            kwargs={'slug': self.object.slug}
        )


class PostDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        post = self.get_object()

        return (
            self.request.user == post.author
            or self.request.user.is_superuser
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Post muvaffaqiyatli o‘chirildi! 🗑️"
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(
            Post,
            slug=self.kwargs['slug'],
            status='PUBLISHED'
        )

        form.instance.post = post
        form.instance.author = self.request.user

        messages.success(
            self.request,
            "Kommentariya muvaffaqiyatli qo‘shildi! 💬"
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'post-detail',
            kwargs={'slug': self.kwargs['slug']}
        )