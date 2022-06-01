from innotter.models import Page, Post


class FollowService:

    def decline_all_followers(self, page: Page, user):
        if page.owner == user:
            page.follow_requests.clear()
            page.save()

    def accept_all_followers(self, page: Page, user):
        if page.owner == user:
            for follow_req in page.follow_requests.all():
                page.followers.add(follow_req)
                page.follow_requests.remove(follow_req)
            page.save()

    def follow(self, page: Page, user):
        if page.is_private:
            page.follow_requests.add(user)
            page.save()
        else:
            page.followers.add(user)
            page.save()

    def unfollow(self, page: Page, user):
        page.follow_requests.remove(user)
        page.followers.remove(user)
        page.save()

    def my_pages(self, user):
        pages = []
        for page in user.pages.all():
            pages.append(page.name)
        return {'my_pages': pages}


class LikeService:
    def like(self, post: Post, user):
        post.liked_by.add(user)
        post.save()

    def unlike(self, post: Post, user):
        post.liked_by.remove(user)
        post.save()
