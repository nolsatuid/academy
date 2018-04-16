from django.contrib import admin

from academy.apps.students.models import Training, Student, TrainingMaterial, TrainingStatus


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'training', 'status')


class TrainingMaterialAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')


class TrainingStatusAdmin(admin.ModelAdmin):
    list_display = ('training_material', 'status', 'user')


admin.site.register(Training)
admin.site.register(Student, StudentAdmin)
admin.site.register(TrainingMaterial, TrainingMaterialAdmin)
admin.site.register(TrainingStatus, TrainingStatusAdmin)
