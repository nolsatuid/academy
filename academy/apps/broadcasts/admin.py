from django.contrib import admin

from .models import Broadcast


@admin.register(Broadcast)
class RatingAdmin(admin.ModelAdmin):
    search_fields = ('title', 'via',)
    list_display = ('title', 'via',)
