from django.urls import path
from .views import (
    CourseListView, CourseDetailView, EnrollCourseView, MyCoursesView,
    CourseContentView, UpdateProgressView, AdminCourseListView,
    AdminCourseDetailView, ModuleViewSet, VideoViewSet,
    CategoryViewSet, TagViewSet
)

urlpatterns = [
    # Public endpoints
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    
    # Student endpoints
    path('courses/<int:pk>/enroll/', EnrollCourseView.as_view(), name='course-enroll'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('my-courses/<int:pk>/', CourseContentView.as_view(), name='course-content'),
    path('progress/<int:video_pk>/', UpdateProgressView.as_view(), name='update-progress'),
    
    # Admin endpoints
    path('admin/courses/', AdminCourseListView.as_view(), name='admin-course-list'),
    path('admin/courses/<int:pk>/', AdminCourseDetailView.as_view(), name='admin-course-detail'),
    path('admin/courses/<int:course_pk>/modules/', ModuleViewSet.as_view(), name='module-list'),
    path('admin/modules/<int:module_pk>/videos/', VideoViewSet.as_view(), name='video-list'),
    path('admin/categories/', CategoryViewSet.as_view(), name='category-list'),
    path('admin/tags/', TagViewSet.as_view(), name='tag-list'),
] 