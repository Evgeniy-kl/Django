from user.models import User
import json


class UserService:
    def show_liked_posts(self, user: User):
        posts = []
        for post in user.likes.all():
            posts.append(post.content)
        return {'liked_posts': posts}
