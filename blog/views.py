from datetime import timezone
from platform import python_version
from urllib.parse import quote_plus

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django import get_version as django_version
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
import requests
from blog.models import Post, Comment
from users.models import User
from .forms import PostUpload, CommentForm


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
    template_name = 'blog/post_update.html'
    model = Post
    fields = ('thumbnail', 'title', 'body')
    context_object_name = 'blog_post'

    def test_func(self):
        return self.get_object().is_author(self.request.user) or self.request.user.is_superuser

    def upload(self, request):
        if request.method == 'POST':
            form = PostUpload(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('blog:home')
        else:
            form = PostUpload()
        return render(request, 'blog/post_detail.html', {
            'form': form
        })


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'blog/post_confirm_delete.html'
    model = Post
    context_object_name = 'post'
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        return self.get_object().is_author(self.request.user) or self.request.user.is_superuser


def make_post(request):
    url = 'https://api.chucknorris.io/jokes/random'
    response = requests.get(url).json()
    title = response.get('value')
    quote = response.get('value')
    thumbnail = response.get('icon_url')
    if request.method == 'POST':
        form = PostUpload(request.POST, request.FILES)
        form.instance.author = request.user

        if form.is_valid():
            form.save()
            return redirect('blog:home')
    else:
        form = PostUpload(initial={'title': title, 'body': quote, 'thumbnail': thumbnail})

    return render(request, 'blog/post_create_special.html', {
        'form': form
    })