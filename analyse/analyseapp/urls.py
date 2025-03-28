from django.urls import path
from .views import top_users, top_or_latest_posts

urlpatterns = [
    path('users/', top_users, name='top_users'),
    path('posts/', top_or_latest_posts, name='top_or_latest_posts'),
]
