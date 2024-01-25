from comments.serializers import LightCommentSerializer
from posts.models import Post, PostComment
from posts.serializers import LightPostSerializer
from users.models import CustomUser
from users.serializers import LightUserSerializer


def get_model_object(name):
    models = {
        "post": Post,
        "post_comment": PostComment,
        "user": CustomUser
    }
    return models.get(name)


def get_serialized_data(model, instance, context):
    serializers = {
        "post": LightPostSerializer,
        "post comment": LightCommentSerializer,
        "user": LightUserSerializer
    }
    serializer = serializers.get(model.name)
    return serializer(instance, context=context).data
