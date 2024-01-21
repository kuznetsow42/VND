from posts.models import Post, PostComment
from users.models import CustomUser


def get_model_object(name):
    models = {
        "post": Post,
        "post_comment": PostComment,
        "user": CustomUser
    }
    return models.get(name)
