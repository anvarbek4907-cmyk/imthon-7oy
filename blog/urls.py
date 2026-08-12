from django.urls import path
from .views import (
    HomeView,
    CategoryView,
    PostDetailView,
    like_post,
    LikedPostsView,
    ProfileView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,      
    CommentDeleteView,
)

urlpatterns = [
    path(  "",  HomeView.as_view(),name="home" ),
    path('profile/', ProfileView.as_view(), name='profile'),

    path( "category/<slug:slug>/", CategoryView.as_view(), name="category"),

    path( "post/create/", PostCreateView.as_view(),name="post-create" ),

    path("post/<slug:slug>/",PostDetailView.as_view(),name="post-detail"),

    path("post/<slug:slug>/update/",PostUpdateView.as_view(),name="post-update" ),

    path( "post/<slug:slug>/delete/",PostDeleteView.as_view(),name="post-delete"),

    path("post/<slug:slug>/comment/",CommentCreateView.as_view(),name="comment-create"),

    path("post/<slug:slug>/like/",like_post, name="like-post"),

    path("liked/",LikedPostsView.as_view(),name="liked-posts" ),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]