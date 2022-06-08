from django.contrib import admin
from innotter.models import Tag, Page, Post


@admin.register(Page)
class DefaultAdmin(admin.ModelAdmin):
    list_filter = ('is_blocked',)


@admin.register(Tag, Post)
class DefaultAdmin(admin.ModelAdmin):
    pass
