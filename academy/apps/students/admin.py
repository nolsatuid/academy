from django.contrib import admin

from academy.apps.students.models import Training, Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'training', 'status')


admin.site.register(Training)
admin.site.register(Student, StudentAdmin)
