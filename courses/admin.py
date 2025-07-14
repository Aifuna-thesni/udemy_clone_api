from django.contrib import admin
from .models import Category, Tag, Course, Module, Video, Enrollment, Progress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)  # Enables multi-select UI
    #list_display = ('title', 'instructor', 'category', 'price', 'is_published', 'created_at')
   # search_fields = ('title', 'description')
    #list_filter = ('category', 'tags', 'is_published')
   # ordering = ('-created_at',)


    def save_model(self, request, obj, form, change):
        if not obj.instructor_id:
            # Make sure the instructor is set to the current logged-in admin user
            obj.instructor = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
        super().save_model(request, obj, form, change)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Module)
admin.site.register(Video)
admin.site.register(Enrollment)
admin.site.register(Progress)

