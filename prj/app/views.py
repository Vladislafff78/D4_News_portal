from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from requests import post

from .filters import PostFilter
from .forms import PostForm
from .models import *


def index(request):
    return render(request, 'index.html')


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticlesList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type_category='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = str(self.model.objects.filter(type_category='AR').count())
        context['filterset'] = self.filterset
        return context


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type_category='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = str(self.model.objects.filter(type_category='NW').count())
        context['filterset'] = self.filterset
        return context


class CreatePost(PermissionRequiredMixin, CreateView):
    permission_required = 'app.add_post'
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = ''


class ArticlesCreate(CreatePost):
    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.post_author = self.request.user.author
        post.type_category = 'AR'
        return super().form_valid(form)


class NewsCreate(CreatePost):
    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.post_author = self.request.user.author
        post.type_category = 'NW'
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    permission_required = 'app.change_post'


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
    permission_required = 'app.delete_post'


def show_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post,
        'post_title': post.post_title,
        'post_text': post.post_text,
        'post_photo': post.post_photo,
        'post_author': post.post_author,
        'post_date': post.post_date,
        'post_date_update': post.post_date_update,
    }

    return render(request, 'app/post.html', context=context)


class CategoryListView(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category)
        return queryset

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
