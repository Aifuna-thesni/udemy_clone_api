from rest_framework import serializers
from .models import Review
from accounts.serializers import UserProfileSerializer

class ReviewSerializer(serializers.ModelSerializer):
    student = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'course', 'student', 'rating', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('course', 'student')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'comment') 