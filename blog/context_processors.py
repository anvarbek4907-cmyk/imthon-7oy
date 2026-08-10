from .models import Post


def recent_posts(request):
    posts = Post.objects.filter(status='PUBLISHED').order_by('-created_at')[:5]
    return {'recent_sidebar_posts': posts}