from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from courses.models import Course, Enrollment
from accounts.permissions import IsAdmin


# Create your views here.

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        return Review.objects.filter(course_id=self.kwargs['course_pk'])
    

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])

        if not Enrollment.objects.filter(student=self.request.user, course=course).exists():
            raise permissions.PermissionDenied("You must be enrolled in the course to leave a review")

        if Review.objects.filter(student=self.request.user, course=course).exists():
            raise permissions.PermissionDenied("You have already reviewed this course")

        self.review = serializer.save(student=self.request.user, course=course)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 💡 Return full review data using ReviewSerializer
        full_data = ReviewSerializer(self.review, context={'request': request})
        return Response(full_data.data, status=status.HTTP_201_CREATED)



class ReviewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Review.objects.all()
        return Review.objects.filter(student=self.request.user)

# Admin Views
class AdminReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
