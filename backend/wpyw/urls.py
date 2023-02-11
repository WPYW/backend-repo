from django.urls import path
from django.contrib import admin
from project import views as project_views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', project_views.ProjectAPIView.as_view()),
]
