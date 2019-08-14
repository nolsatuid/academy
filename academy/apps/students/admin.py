from django.contrib import admin

from academy.apps.students.models import Training, Student, TrainingMaterial, TrainingStatus


class StudentAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'user__username',)
    list_display = ('user', 'training', 'status')
    raw_id_fields = ('user',)


class TrainingMaterialAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')


class TrainingStatusAdmin(admin.ModelAdmin):
    list_display = ('training_material', 'status', 'user')
    search_fields = ('user__username', 'user__email', 'training_material__code')


admin.site.register(Training)
admin.site.register(Student, StudentAdmin)
admin.site.register(TrainingMaterial, TrainingMaterialAdmin)
admin.site.register(TrainingStatus, TrainingStatusAdmin)
