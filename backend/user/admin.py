from django.contrib import admin
from user.models import User


@admin.register(User)
class DefaultAdmin(admin.ModelAdmin):
    list_filter = ('role',)
