from django.contrib import admin

from academy.apps.offices.models import LogoPartner, LogoSponsor, BannerInfo


class AdminLogoPartners(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_visible')


class AdminLogoSponsor(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_visible')


class AdminBannerInfo(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')


admin.site.register(LogoPartner, AdminLogoPartners)
admin.site.register(LogoSponsor, AdminLogoSponsor)
admin.site.register(BannerInfo, AdminBannerInfo)
