def get_user_relations(request, obj):
    user = request.user
    user_relation = {"like": False, "bookmark": False}
    if user.is_anonymous:
        return user_relation
    user_relation["like"] = user in obj.likes.all()
    user_relation["bookmark"] = user in obj.bookmarks.all()
    return user_relation
