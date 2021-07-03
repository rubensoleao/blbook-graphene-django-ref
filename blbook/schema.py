# cookbook/schema.py
# pylint: disable=no-self-argument,redefined-builtin
import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required

from blbook.user.schemas import UserType
from blbook.user.mutations import CreateUser, FollowUser, UnfollowUser


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    follow_me = graphene.List(UserType)
    following = graphene.List(UserType)

    def resolve_all_users(root, info):
        return User.objects.all()

    @login_required
    def resolve_follow_me(root, info):
        user = info.context.user
        followers = []
        for follower in user.followed_by.all():
            followers.append(follower.user)

        return followers

    @login_required
    def resolve_following(root, info):
        user = info.context.user
        followers = []
        for follower in user.following.all():
            followers.append(follower.user_followed)

        return followers


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
