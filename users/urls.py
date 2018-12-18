from django.urls import path

from users.views import UserDetailView, UserListView, UserRedirectView, UserUpdateView, add_follower
from . import views

app_name = 'users'

urlpatterns = [
    path('', view=UserListView.as_view(), name='list'),
    path('~redirect/', view=UserRedirectView.as_view(), name='redirect'),
    path('<str:username>/follow/', views.add_follower, name='follow'),
    path('<str:username>/unfollow/', views.unffolow, name='unfollow'),
    path('<str:username>/', view=UserDetailView.as_view(), name='detail'),
    path('<str:username>/edit', view=UserUpdateView.as_view(), name='changeDetails'),
]
