# cookbook/schema.py
import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from blbook.posts.models import Post


class UserType(DjangoObjectType):
    class Meta:
        model=User
        fields=("id", "name", "email")

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "text", "posted_by")
        
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)

    def resolve_all_users(root, info):
        # We can easily optimize query count in the resolve method
        return User.objects.all()

schema = graphene.Schema(query=Query)