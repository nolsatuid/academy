from django.contrib import admin

from .models import LogTrainingStatus


class LogTrainingStatusAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email')
    list_display = ('user', 'code', 'status')


admin.site.register(LogTrainingStatus, LogTrainingStatusAdmin)