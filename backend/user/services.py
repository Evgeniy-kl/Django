from user.models import User


class BlockService:
    @staticmethod
    def block_all_pages(user: User, request):
        pages = user.pages
        print(pages.values_list('uuid'))
        for page in pages.all():
            page.is_blocked = bool(request.data['is_blocked'])
            page.save()


class UserService:
    @staticmethod
    def show_liked_posts(user: User):
        return {'liked_posts': user.likes.values_list('content', flat=True)}

    @staticmethod
    def dashboard(user: User):
        # pages
        followed_pages = user.follows.all()
        my_pages = user.pages.all()
        # posts
        my_posts = my_pages.values_list('posts', flat=True)
        followed_posts = followed_pages.values_list('posts', flat=True)
        dashboard_posts = my_posts | followed_posts
        return {'dashboard': dashboard_posts}
