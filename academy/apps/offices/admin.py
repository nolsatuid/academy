from django.contrib import admin

from academy.apps.offices.models import (
    LogoPartner, LogoSponsor, BannerInfo, Page, Setting, FAQ, CategoryPage, Banner
)


class AdminLogoPartners(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_visible')


class AdminLogoSponsor(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_visible')


class AdminBannerInfo(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')


class AdminPage(admin.ModelAdmin):
    list_display = ('title', 'is_visible', 'status', 'group')


class AdminSetting(admin.ModelAdmin):
    list_display = (
        'site_name', 'color_theme', 'sidebar_color', 'footer_title',
        'hide_logo'
    )


class AdminFAQ(admin.ModelAdmin):
    list_display = (
        'question', 'answer', 'display_order'
    )


class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'slug')


class AdminBanner(admin.ModelAdmin):
    list_display = ('title', 'link', 'show_web', 'show_app')


admin.site.register(LogoPartner, AdminLogoPartners)
admin.site.register(LogoSponsor, AdminLogoSponsor)
admin.site.register(BannerInfo, AdminBannerInfo)
admin.site.register(Page, AdminPage)
admin.site.register(Setting, AdminSetting)
admin.site.register(FAQ, AdminFAQ)
admin.site.register(CategoryPage, AdminCategory)
admin.site.register(Banner, AdminBanner)
