# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Profile, Instructor, Inbox


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': (
            'role', 'is_active', 'is_staff', 'is_superuser', 'registered_via', 'has_valid_email',
            'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'is_active', 'is_staff', 'registered_via', 'has_valid_email')


class UserProfile(admin.ModelAdmin):
    search_fields = ('user__username',)


class InstructorAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)


class InboxAdmin(admin.ModelAdmin):
    search_fields = ('user__username','subject',)
    list_display = ('user', 'subject', 'is_read', 'sent_date')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, UserProfile)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Inbox, InboxAdmin)
