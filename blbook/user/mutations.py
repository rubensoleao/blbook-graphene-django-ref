# pylint: disable=no-self-argument,redefined-builtin

import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from blbook.user.models import Follow


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
            return FollowUser(success=False, error_message="Authentication credentials were not provided")

        try:
            user_followed = User.objects.get(id=id)
        except Exception:
            return FollowUser(success=False, errorMessage="Unable to find request user to follow")

        try:
            Follow.objects.get_or_create(user=user, user_followed=user_followed)
        except Exception as e:
            return FollowUser(success=False, error_message=str(e))

        return FollowUser(success=True, error_message=False)


class UnfollowUser(graphene.Mutation):
    success = graphene.Boolean()
    error_message = graphene.String()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        user = info.context.user

        if not user.is_authenticated:
            return UnfollowUser(success=False, error_message="Authentication credentials were not provided")
        try:
            followed = Follow.objects.get(user=user, user_followed__id=id)
            if not followed:
                return UnfollowUser(success=False, error_message="The user does not follow selected user")
            else:
                followed.delete()
        except Exception as e:
            return UnfollowUser(success=False, error_message=str(e))

        return UnfollowUser(success=True, error_message=False)
