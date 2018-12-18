from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing_page'),
    path('blog/', views.HomeView.as_view(), name='home'),
    path('info/', views.InfoView.as_view(), name='info'),
    path('post/create-text/', views.TextPostCreateView.as_view(), name='text_post_create'),
    path('post_create_special/', views.MakeSpecialPost.as_view(), name='post_create'),
    path('post/<pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<pk>/<comment_id>/reply/', views.PostChildComment.as_view(), name='replyToComment'),
    path('post/<pk>/update', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
]
