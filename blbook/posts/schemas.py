from graphene_django import DjangoObjectType
from .models import Post

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "text", "posted_by")
