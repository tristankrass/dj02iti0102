from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions import Lower
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from blog.models import Comment, Post

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'blog_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['active'] = 'user-detail'
        context['nr_of_posts'] = Post.objects.filter(author=self.object).count()
        context['blog_posts'] = Post.objects.filter(author=self.object)
        context['nr_of_comments'] = Comment.objects.filter(author=self.object).count()
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'users/changeDetails.html'
    fields = ('username', 'avatar')
    context_object_name = 'blog_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    permission_denied_message = 'Hey Mate! No cookie for you!'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'blog_users'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().order_by(Lower('username'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['active'] = 'user-list'
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail', kwargs={'username': self.request.user.username})


def add_follower(request, username):
    to_follow = User.objects.filter(username=username).first()
    if request.user != to_follow:
        logged_in_user = User.objects.filter(username=request.user).first()
        logged_in_user.follows.add(to_follow)
        to_follow.save()
        logged_in_user.save()

    return render(request, 'users/follow.html')


def unffolow(request, username):
    to_follow = User.objects.filter(username=username).first()
    if request.user != to_follow:
        request.user.follows.remove(to_follow)
        to_follow.save()
        request.user.save()
    else:
        messages.error(request, 'You are not allowed to do that.')

    return render(request, 'users/unfollow.html', {'user': to_follow})
