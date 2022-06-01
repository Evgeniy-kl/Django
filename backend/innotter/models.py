from django.db import models
from core.mixins.models import TimestampMixin
from django.db.models import Q
import datetime


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class PageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(is_blocked=False),
            Q(
                Q(unblock_date__lte=datetime.datetime.now()) |
                Q(unblock_date=None)
            )
        )


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='pages')

    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('user.User', related_name='follows', null=True, blank=True)

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('user.User', related_name='requests', null=True, blank=True)

    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)

    active_pages = PageManager()
    objects = models.Manager()

    def __str__(self):
        return self.name


class Post(TimestampMixin):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    reply_to = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, related_name='replies')
    liked_by = models.ManyToManyField('user.User', related_name='likes', null=True, blank=True)

    def __str__(self):
        return self.content
