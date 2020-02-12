from django.contrib import admin

from academy.apps.offices.models import LogoPartner, LogoSponsor, BannerInfo, Page


class AdminLogoPartners(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_visible')


class AdminLogoSponsor(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_visible')


class AdminBannerInfo(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')


class AdminPage(admin.ModelAdmin):
    list_display = ('title', 'is_visible', 'status')


admin.site.register(LogoPartner, AdminLogoPartners)
admin.site.register(LogoSponsor, AdminLogoSponsor)
admin.site.register(BannerInfo, AdminBannerInfo)
admin.site.register(Page, AdminPage)
