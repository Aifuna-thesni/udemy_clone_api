from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from .models import Enrollment, Course
from .serializers import EnrollmentSerializer
from .models import Category, Tag, Course, Module, Video, Enrollment, Progress
from .serializers import (
    CategorySerializer, TagSerializer, CourseListSerializer, CourseDetailSerializer,
    CourseCreateSerializer, ModuleSerializer, VideoSerializer, EnrollmentSerializer,
    ProgressSerializer
)
from accounts.permissions import IsAdmin

# Public Views
class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category__name', 'tags__name']
    ordering_fields = ['created_at', 'price', 'rating']
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True)
        category = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if category:
            queryset = queryset.filter(category__id=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseDetailSerializer
    permission_classes = (permissions.AllowAny,)

# Student Views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course, Enrollment
from .serializers import EnrollmentSerializer

class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        student = request.user

        # Already enrolled?
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response({'error': 'You are already enrolled in this course.'}, status=400)

        # Create enrollment
        enrollment = Enrollment.objects.create(student=student, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=201)


class MyCoursesView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

class CourseContentView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        enrollment = get_object_or_404(Enrollment, course=course, student=self.request.user)
        return course

class UpdateProgressView(generics.UpdateAPIView):
    serializer_class = ProgressSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        video = get_object_or_404(Video, pk=self.kwargs['video_pk'])
        enrollment = get_object_or_404(
            Enrollment,
            course=video.module.course,
            student=self.request.user
        )
        progress, created = Progress.objects.get_or_create(
            enrollment=enrollment,
            video=video
        )
        return progress

# Admin Views
class AdminCourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseListSerializer
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class AdminCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class ModuleViewSet(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    
    def get_queryset(self):
        return Module.objects.filter(course_id=self.kwargs['course_pk'])
    
    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        serializer.save(course=course)

class VideoViewSet(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        return Video.objects.filter(module_id=self.kwargs['module_pk'])
    
    def perform_create(self, serializer):
        module = get_object_or_404(Module, pk=self.kwargs['module_pk'])
        serializer.save(module=module)

class CategoryViewSet(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class TagViewSet(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
