from django.contrib import admin

from users.models import User

#admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email', 'is_active', 'is_staff', 'is_superuser']



