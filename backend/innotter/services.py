from innotter.models import Post
from innotter.models import Page
from innotter.tasks import send_mail_to
from innotter.producer import pusblish
import pika

class ValidateFileFormat:
    @staticmethod
    def is_valid_file(file_name: str):
        valid_formats = ['png', 'jpg', 'jpeg']
        file_format = file_name.split('.')[-1]
        if file_format in valid_formats:
            return True
        else:
            return False


class FollowService:
    @staticmethod
    def decline_all_followers(page: Page, user):
        if page.owner == user:
            page.follow_requests.clear()
            page.save()

    @staticmethod
    def accept_all_followers(page: Page, user):
        if page.owner == user:
            for follow_req in page.follow_requests.all():
                page.followers.add(follow_req)
                page.follow_requests.remove(follow_req)
            page.save()

    @staticmethod
    def follow(page: Page, user):
        if page.owner == user:
            return 'You are owner!'
        if page.is_private:
            page.follow_requests.add(user)
            page.save()
        else:
            page.followers.add(user)
            ###
            pusblish({'user': str(user), 'method': 'qty_followers'})
            page.save()
        return 'Followed'

    @staticmethod
    def unfollow(page: Page, user):
        if page.owner == user:
            return 'You are owner!'
        page.follow_requests.remove(user)
        page.followers.remove(user)
        page.save()
        return 'Unfollowed'

    @staticmethod
    def my_pages(user):
        return {'my_pages': user.pages.values_list('name', flat=True)}

    @staticmethod
    def notification_to_subscribers(page: int):
        page_to_send = Page.objects.get(pk=page)
        for follower in page_to_send.followers.all():
            send_mail_to('New post', 'New post by {}'.format(page_to_send.name), follower.email)


class LikeService:
    @staticmethod
    def like(post: Post, user):
        post.liked_by.add(user)
        ###
        pusblish({'user': str(user), 'method': 'qty_likes'})
        post.save()

    @staticmethod
    def unlike(post: Post, user):
        post.liked_by.remove(user)
        post.save()


class RabbitManage:

    def __init__(self, host, port: int, virtualhost, username, password):
        self.host = host
        self.port = port
        self.virtualhost = virtualhost
        self.username = username
        self.password = password

    def connect(self):
        creds = pika.PlainCredentials(self.username, self.password)
        params = pika.ConnectionParameters(self.host,
                                           self.port,
                                           self.virtualhost,
                                           creds)

        connection = pika.BlockingConnection(params)

        return connection.channel()
