import graphene
from django.contrib.auth import get_user_model
from .schemas import PostType
from .models import Post

class PostMessage(graphene.Mutation):
    success = graphene.Boolean()
    error_message = graphene.String()
    message = graphene.Field(PostType)

    class Arguments:
        text = graphene.String()

    def mutate(self, info, text):
        user = info.context.user

        if not user.is_authenticated:
            return PostMessage(success=False, error_message="Authentication credentials were not provided", meessage=None)

        new_post = None
        try:
            new_post = Post(text=text, posted_by=user)
            new_post.save()
        except Exception as e:
            return PostMessage(success=False, error_message=str(e), message=None)

        return PostMessage(success=True, error_message=False, message=new_post)