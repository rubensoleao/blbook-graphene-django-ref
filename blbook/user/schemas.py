# pylint: disable=no-self-argument,redefined-builtin

import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    follower_count = graphene.Int()
    follows_count = graphene.Int()

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def resolve_follows_count(self, info):
        me = User.objects.get(id=self.id)
        return me.following.count()

    def resolve_follower_count(self, info):
        me = User.objects.get(id=self.id)
        return me.followed_by.all().count()
