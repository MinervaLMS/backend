from django.contrib import admin

from .models import Course, Module, Material, Enrollment

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

class MaterialInline(admin.StackedInline):
    model = Material
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "alias",)
    search_fields = ("name", "alias")
    inlines = [ModuleInline]

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course_id',)
    list_filter = ('course_id',)
    search_fields = ('name', 'course__name')
    inlines = [MaterialInline]

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'material_type', 'module_id', 'is_extra',)
    list_filter = ('material_type',)
    search_fields = ('name', 'module_id')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_id', 'user_id', 'enrollment_date',)
    list_filter = ('course_id',)
    search_fields = ('course_id', 'user_id')

admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)