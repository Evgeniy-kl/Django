from innotter.models import Page, Post


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
        if page.is_private:
            page.follow_requests.add(user)
            page.save()
        else:
            page.followers.add(user)
            page.save()

    @staticmethod
    def unfollow(page: Page, user):
        page.follow_requests.remove(user)
        page.followers.remove(user)
        page.save()

    @staticmethod
    def my_pages(user):
        return {'my_pages': user.pages.values_list()}


class LikeService:
    @staticmethod
    def like(post: Post, user):
        post.liked_by.add(user)
        post.save()

    @staticmethod
    def unlike(post: Post, user):
        post.liked_by.remove(user)
        post.save()
