from django.contrib import admin

from .models import Grouping, RightsShell, User


@admin.register(Grouping)
class GroupingAdmin(admin.ModelAdmin):
    pass


@admin.register(RightsShell)
class RightsShellAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
