from django.urls import path, include
from rest_framework import routers
from .views import AuthorViewset, CategoryViewset, PostViewset, CommentViewset
from .views import author_posts, publish_post, published_posts_list, approve_comment, unapproved_comments, post_comments

router = routers.DefaultRouter()
router.register(r'author', AuthorViewset)
router.register(r'categories', CategoryViewset)
router.register(r'posts', PostViewset)
router.register(r'comments', CommentViewset)

urlpatterns = [
    path('', include(router.urls)),  
    path('author/<int:pk>/posts', author_posts),
    path('posts/<int:pk>/publish', publish_post),
    path('posts/published', published_posts_list),
    path('comments/<int:pk>/approve', approve_comment),
    path('comments/pending', unapproved_comments),
    path('posts/<int:pk>/comments', post_comments)
]