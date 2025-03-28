from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Post
from .serializers import UserSerializer, PostSerializer

@api_view(['GET'])
def top_users(request):
    """Fetch top 5 users with highest number of posts"""
    top_users = User.objects.order_by('-post_count')[:5]
    serializer = UserSerializer(top_users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def top_or_latest_posts(request):
    """Fetch top or latest posts based on query parameter"""
    post_type = request.GET.get('type', 'latest')  # Default to 'latest'

    if post_type == 'popular':
        posts = Post.objects.order_by('-comment_count')[:5]
    else:
        posts = Post.objects.order_by('-created_at')[:5]

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
