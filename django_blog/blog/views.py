from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import F

from .models import Post, Category, Tag
from .forms import CommentForm


class PostListView(ListView):
    """Вьюха для вывода постов на главной странице"""

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['popular_post'] = Post.objects.order_by('-views').select_related('category').first()
        return context


class PostsByCategory(ListView):
    """Вьюха для вывода постов для определенной категории"""

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Category: ' + Category.objects.get(slug=self.kwargs['slug']).title
        context['popular_post'] = Post.objects.filter(
            category__slug=self.kwargs['slug']
        ).order_by('-views').select_related('category').first()
        return context


class PostDetailView(DetailView):
    """Вьюха для детального просмотра одного поста"""

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        post = Post.objects.filter(slug=self.kwargs['slug']).select_related('category')
        post.update(views=F('views') + 1)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context


class PostsByTag(ListView):
    """Вьюха для вывода постов по тегу"""

    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tag: ' + Tag.objects.get(slug=self.kwargs['slug']).title
        context['popular_post'] = Post.objects.filter(
            tags__slug=self.kwargs['slug']
        ).order_by('-views').select_related('category').first()
        return context


class Search(ListView):
    """Вьюха для поиска по постам"""

    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('search'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f'search={self.request.GET.get("search")}&'
        return context


class AddComment(View):
    """Отзывы"""

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())
