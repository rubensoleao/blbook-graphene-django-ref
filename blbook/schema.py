# cookbook/schema.py
# pylint: disable=no-self-argument,redefined-builtin
import graphene
import graphql_jwt
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from blbook.posts.models import Post
from blbook.posts.mutations import PostMessage
from blbook.posts.schemas import FeedType
from blbook.user.mutations import CreateUser, FollowUser, UnfollowUser
from blbook.user.schemas import UserType


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    follow_me = graphene.List(UserType)
    following = graphene.List(UserType)
    feed = graphene.Field(FeedType, limit=graphene.Int(), offset=graphene.Int())

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

    @login_required
    def resolve_feed(root, info, limit, offset):
        user = info.context.user
        following_ids = user.following.values_list('user_followed__id', flat=True).all()
        posts = Post.objects.filter(posted_by__id__in=following_ids).order_by("-posted_at")
        paginator = Paginator(posts, limit)
        page = int(offset / limit) + 1

        return FeedType(
            page_info={"total_pages": paginator.num_pages, "page": page},
            messages=paginator.page(page),
        )


class Mutation(graphene.ObjectType):
    login = (
        graphql_jwt.ObtainJSONWebToken.Field()
    )  # TODO: standerdize parameters for this query i.e. ErrorMessage
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register = CreateUser.Field()
    follow = FollowUser.Field()
    unfollow = UnfollowUser.Field()
    post_message = PostMessage.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
