from django.contrib import admin
from innotter.models import Tag, Page, Post


@admin.register(Tag, Page, Post)
class DefaultAdmin(admin.ModelAdmin):
    pass
