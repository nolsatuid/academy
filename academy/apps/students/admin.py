from django.contrib import admin

from academy.apps.students.models import Training, Student, TrainingMaterial


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'training', 'status')


class TrainingMaterialAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')


admin.site.register(Training)
admin.site.register(Student, StudentAdmin)
admin.site.register(TrainingMaterial, TrainingMaterialAdmin)
