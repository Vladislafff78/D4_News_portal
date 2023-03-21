from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='about'),
    path('posts/', PostsList.as_view(), name='posts'),
    path('create_post', CreatePost.as_view(), name='create_post'),
    path('post/<int:post_id>/', show_post, name='post'),
    ]

