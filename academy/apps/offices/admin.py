from django.contrib import admin

from academy.apps.offices.models import LogoPartner, LogoSponsor


class AdminLogoPartners(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_visible')


class AdminLogoSponsor(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_visible')


admin.site.register(LogoPartner, AdminLogoPartners)
admin.site.register(LogoSponsor, AdminLogoSponsor)
