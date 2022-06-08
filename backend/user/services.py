from django.db.models import Q
from user.models import User
from innotter.models import Post


class BlockService:
    @staticmethod
    def block_all_pages(user: User, request):
        user.pages.update(is_blocked=bool(request.data['is_blocked']))


class UserService:
    @staticmethod
    def show_liked_posts(user: User):
        return {'liked_posts': user.likes.values_list('content', flat=True)}

    @staticmethod
    def dashboard(user: User):
        dashboard_posts = Post.objects.filter(
            Q(page__owner=user) |
            Q(page__followers=user)
        ).all()
        return {'dashboard': dashboard_posts.values_list('id', flat=True)}
