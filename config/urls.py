from django.urls import path
from blog.views import (
    PostDetailView,
    PostCreateView,
)

from django.contrib import admin
from django.urls import path, include
from blog.views import PostDetailView

urlpatterns = [
    # ...

    path(
        "post/create/",
        PostCreateView.as_view(),
        name="post-create"
    ),

    path(
        "post/<int:pk>/",
        PostDetailView.as_view(),
        name="post-detail"
    ),

    path("admin/", admin.site.urls),

    path("users/", include("users.urls")),

    path("", include("blog.urls")),
]