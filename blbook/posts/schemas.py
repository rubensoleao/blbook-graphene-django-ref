import graphene
from graphene_django import DjangoObjectType
from .models import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "text", "posted_by", "posted_at")


class PageType(graphene.ObjectType):
    total_pages = graphene.Int()
    page = graphene.Int()


class FeedType(graphene.ObjectType):
    messages = graphene.List(PostType)
    page_info = graphene.Field(PageType)
