from django.contrib import admin
from django.contrib.auth import get_user_model

user_model = get_user_model()
admin.site.unregister(user_model)


@admin.register(user_model)
class UserAdmin(admin.ModelAdmin):

    list_display = [
        'username',
        'email',
    ]

    ordering = [
        'username',
    ]
    search_fields = [
        'username',
        'email',
    ]
    list_filter = [
        'username',
        'email',
    ]
