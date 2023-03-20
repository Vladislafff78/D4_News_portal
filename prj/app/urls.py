from django.urls import path
from .import views
from .views import show_post

urlpatterns = [
    path('', views.index, name='about'),
    path('posts', views.posts, name='posts'),
    path('create_post', views.CreatePost.as_view(), name='create_post'),
    path('post/<int:post_id>/', show_post, name='post'),
    ]

