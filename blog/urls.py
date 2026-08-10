from django.urls import path

from .views import (
    HomeView,
    CategoryView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    like_post,
    LikedPostsView,
)

urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home"
    ),

    path(
        "category/<slug:slug>/",
        CategoryView.as_view(),
        name="category"
    ),

    path(
        "post/create/",
        PostCreateView.as_view(),
        name="post-create"
    ),

    path(
        "post/<slug:slug>/",
        PostDetailView.as_view(),
        name="post-detail"
    ),

    path(
        "post/<slug:slug>/update/",
        PostUpdateView.as_view(),
        name="post-update"
    ),

    path(
        "post/<slug:slug>/delete/",
        PostDeleteView.as_view(),
        name="post-delete"
    ),

    path(
        "post/<slug:slug>/comment/",
        CommentCreateView.as_view(),
        name="comment-create"
    ),

    path(
        "post/<slug:slug>/like/",
        like_post,
        name="like-post"
    ),

    path(
        "liked/",
        LikedPostsView.as_view(),
        name="liked-posts"
    ),
]