from django.urls import path
from .views import (
    ReviewListView, ReviewCreateView, ReviewUpdateDeleteView,
    AdminReviewListView
)

urlpatterns = [
    # Public endpoints
    path('courses/<int:course_pk>/reviews/', ReviewListView.as_view(), name='review-list'),
    
    # Student endpoints
    path('courses/<int:course_pk>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', ReviewUpdateDeleteView.as_view(), name='review-update-delete'),
    
    # Admin endpoints
    path('admin/reviews/', AdminReviewListView.as_view(), name='admin-review-list'),
] 