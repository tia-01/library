# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AuthorSerializer, CategorySerializer, PostSerializer, CommentSerializer
from .models import Author, Category, Post, Comment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.

class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.select_related(
        "author"
    ).prefetch_related(
        "categories",
        "comments"
    )
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_published", "author", "categories"]
    search_fields = ["title"]
    
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@api_view(["GET"])
def author_posts(request, pk=None):
    posts = Post.objects.filter(author_id=pk)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def published_posts_list(request):
    posts = Post.objects.filter(is_published=True)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(["PATCH"])
def publish_post(request, pk=None):
    post = get_object_or_404(Post, id=pk)
    if post.is_published:
            return Response(
                {"detail": "Post is already published."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    post.is_published = True
    post.save(update_fields=["is_published"])
    return Response(
        {"detail": "Post published successfully."},
        status=status.HTTP_200_OK,
    )
# Post.objects.filter(is_published=False).update(is_published=True)

@api_view(["PATCH"])
def approve_comment(request, pk=None):
    comment = get_object_or_404(Comment, id=pk)
    if comment.is_approved:
            return Response(
                {"detail": "Comment is already approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    comment.is_approved = True
    comment.save(update_fields=["is_approved"])
    return Response(
        {"detail": "Comment approved successfully."},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def unapproved_comments(request):
    comments = Comment.objects.filter(is_approved=False)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def post_comments(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    
    if not post.is_published:
        return Response(
            {"error": "Cannot create a comment on an unpublished post."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(post=post)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
