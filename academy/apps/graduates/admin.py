from django.contrib import admin

from .models import Graduate, Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    search_fields = ('respondent_name', 'graduate__user__username',)
    list_display = ('respondent_name', 'rating', 'graduate',)


admin.site.register(Graduate)
