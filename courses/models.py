from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_teaching')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    tags = models.ManyToManyField(Tag, related_name='courses')
    thumbnail = models.ImageField(upload_to='tag_thumbnails/', null=True, blank=True)  
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    students = models.ManyToManyField(User, through='Enrollment', related_name='courses_enrolled')
    
    def __str__(self):
        return self.title
    
    @property
    def rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)
    
    @property
    def total_students(self):
        return self.students.count()

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Video(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='course_videos/')
    duration = models.PositiveIntegerField(help_text='Duration in seconds')
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.email} enrolled in {self.course.title}"

class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress')
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    last_watched_at = models.DateTimeField(null=True, blank=True)
    watch_time = models.PositiveIntegerField(default=0, help_text='Time watched in seconds')
    
    class Meta:
        unique_together = ['enrollment', 'video']
    
    def __str__(self):
        return f"{self.enrollment.student.email} - {self.video.title}"
