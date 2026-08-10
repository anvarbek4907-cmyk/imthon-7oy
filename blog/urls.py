from django.urls import path

from .views import (
    HomeView,
    CategoryView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
)


urlpatterns = [
    # Bosh sahifa
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),

    # Kategoriya
    path(
        "category/<slug:slug>/",
        CategoryView.as_view(),
        name="category",
    ),

    # Yangi post yaratish
    path(
        "post/create/",
        PostCreateView.as_view(),
        name="post-create",
    ),

    # Postni ko'rish
    path(
        "post/<slug:slug>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),

    # Postni tahrirlash
    path(
        "post/<slug:slug>/update/",
        PostUpdateView.as_view(),
        name="post-update",
    ),

    # Postni o'chirish
    path(
        "post/<slug:slug>/delete/",
        PostDeleteView.as_view(),
        name="post-delete",
    ),

    # Kommentariya qo'shish
    path(
        "post/<slug:slug>/comment/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
]