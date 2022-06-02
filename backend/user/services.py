from user.models import User


class UserService:
    @staticmethod
    def show_liked_posts(user: User):
        return {'liked_posts': user.likes.values_list('content', flat=True)}
