# cookbook/schema.py
# pylint: disable=no-self-argument,redefined-builtin
import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from blbook.posts.models import Follow

from blbook.posts.models import Post

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


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "text", "posted_by")


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    follow_me = graphene.List(UserType)

    def resolve_all_users(root, info):
        # We can easily optimize query count in the resolve method
        return User.objects.all()

    @login_required
    def resolve_follow_me(root, info):
        user = info.context.user
        followers = []
        for follower in user.followed_by.all():
            followers.append(follower.user)
 

        return followers


class CreateUser(graphene.Mutation):
    success = graphene.Boolean()
    error_message = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        try:
            user = get_user_model()(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
        except Exception as e:
            return CreateUser(success=False, error_message=str(e))

        return CreateUser(success=True, error_message=False)

class FollowUser(graphene.Mutation):
    success = graphene.Boolean()
    error_message = graphene.String()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        user = info.context.user

        if not user.is_authenticated:
            return CreateUser(success=False, error_message="Authentication credentials were not provided")

        try:
            user_followed = User.objects.get(id=id)
        except Exception:
            return FollowUser(success=False, errorMessage="Unable to find request user to follow")

        try:
            Follow.objects.get_or_create(user=user, user_followed=user_followed)
        except Exception as e:
            return CreateUser(success=False, error_message=str(e))

        return CreateUser(success=True, error_message=False)

class UnfollowUser(graphene.Mutation):
    success = graphene.Boolean()
    error_message = graphene.String()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        user = info.context.user

        if not user.is_authenticated:
            return CreateUser(success=False, error_message="Authentication credentials were not provided")
        try:
            followed = Follow.objects.get(user=user, user_followed__id=id)
            if not followed:
                return CreateUser(success=False, error_message="The user does not follow selected user")
            else:
                followed.delete()
        except Exception as e:
            return CreateUser(success=False, error_message=str(e))

        return CreateUser(success=True, error_message=False)



class Mutation(graphene.ObjectType):
    login = (
        graphql_jwt.ObtainJSONWebToken.Field()
    )  # TODO: standerdize parameters for this query i.e. ErrorMessage
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register = CreateUser.Field()
    follow = FollowUser.Field()
    unfollow = UnfollowUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
