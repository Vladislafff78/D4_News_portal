from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='about'),


    path('posts/', PostsList.as_view(), name='posts'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('articles/', ArticlesList.as_view(), name='articles_list'),


    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),


    path('create_post', CreatePost.as_view(), name='create_post'),
    path('post/<int:post_id>/', show_post, name='post'),

    path('post/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),


    ]

