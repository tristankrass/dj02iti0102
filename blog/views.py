from platform import python_version
from django.shortcuts import render, redirect
from django import get_version as django_version
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
import requests
from blog.models import Post, Comment
from users.models import User
from .forms import PostUpload


class HomeView(ListView):
    template_name = 'blog/home.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['active'] = 'blog-home'
        return context


class InfoView(TemplateView):
    template_name = 'blog/info.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'active': 'blog-info',
            'python_version': python_version(),
            'django_version': django_version(),
            'number_of_users': User.objects.count(),
            'number_of_posts': Post.objects.count(),
            'number_of_comments': Comment.objects.count(),
        })
        return context


class PostDisplay(ModelFormMixin, DetailView):
    template_name = 'blog/post_detail.html'
    model = Post
    fields = ('body',)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('created_timestamp')
        return qs


class PostComment(CreateView):
    template_name = 'blog/post_detail.html'
    model = Comment
    fields = ('body', 'parent')

    def post(self, request, *args, **kwargs):
        print(self.request.POST.get('parent_id'))
        self.post_obj = Post.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.parent_id = self.request.POST.get('parent_id')
        parent_obj = None
        if form.parent_id:
            parent_qs = Comment.objects.filter(id=form.parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        form.parent_obj = parent_obj
        form.instance.post = self.post_obj
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post_obj
        return context

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_obj.pk})


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class TextPostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/post_create.html'
    model = Post
    fields = ('title', 'body', 'thumbnail')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ('title', 'body', 'thumbnail')
    context_object_name = 'blog_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().is_author(self.request.user) or self.request.user.is_superuser


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'blog/post_confirm_delete.html'
    model = Post
    context_object_name = 'post'
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        return self.get_object().is_author(self.request.user) or self.request.user.is_superuser


class MakeSpecialPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create_special.html'
    fields = ('title', 'body', 'thumbnail')
    url = 'https://api.chucknorris.io/jokes/random'
    response = requests.get(url).json()
    quote = response.get('value')
    title = " ".join(quote.split()[:3])
    thumbnail = response.get('icon_url')
    context_object_name = 'blog_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        return {
            'title': self.title,
            'body': self.quote
        }

    def test_func(self):
        return self.get_object().is_author(self.request.user) or self.request.user.is_superuser
