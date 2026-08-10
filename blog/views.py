from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Post, Category, Comment
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

        if sort == 'views':
            posts = posts.order_by('-views_count')
        elif sort == 'old':
            posts = posts.order_by('created_at')
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
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        context["similar_posts"] = Post.objects.exclude(
            pk=post.pk
        ).order_by("-created_at")[:3]

        context["comments"] = post.comments.all()

        context["comment_form"] = CommentForm()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'PUBLISHED'   # ← endi darhol nashr qilinadi
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy(
            'post-detail',
            kwargs={'slug': self.object.slug}
        )


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser


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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'post-detail',
            kwargs={'slug': self.kwargs['slug']}
        )