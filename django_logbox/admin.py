from django.contrib import admin

from .models import ServerLog


@admin.register(ServerLog)
class ServerLogAdmin(admin.ModelAdmin):
    pass
