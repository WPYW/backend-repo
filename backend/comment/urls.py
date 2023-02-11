from django.urls import path
from . import views

urlpatterns = [
  path('', views.CommentAPIView.as_view()),
  path('<int:pk>/',views.CommentDetailAPIView.as_view()),
    
]