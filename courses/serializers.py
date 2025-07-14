from rest_framework import serializers
from .models import Category, Tag, Course, Module, Video, Enrollment, Progress
from accounts.serializers import UserProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    video_file = serializers.FileField(required=True)

    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'video_file', 'duration', 'order')


class ModuleSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order', 'videos')

class CourseListSerializer(serializers.ModelSerializer):
    instructor = UserProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)
    total_students = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'instructor', 'category', 'tags', 
                 'thumbnail', 'price', 'rating', 'total_students', 'created_at')
        

class CourseDetailSerializer(CourseListSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + ('modules', 'is_published')


class CourseCreateSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0  
    )


    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'category', 'tags', 'thumbnail', 'price', 'is_published')
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        course = Course.objects.create(**validated_data)
        course.tags.set(tags)
        return course


class EnrollmentSerializer(serializers.ModelSerializer):
    course_details = CourseListSerializer(source='course', read_only=True)

    class Meta:
        model = Enrollment
        fields = (
            'id',
            'course_details',  # show course info
            'date_enrolled',
            'is_completed',
            'progress'
        )


class ProgressSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    
    class Meta:
        model = Progress
        fields = ('id', 'video', 'watched', 'last_watched_at', 'watch_time') 