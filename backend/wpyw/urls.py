from django.urls import include, path
from django.contrib import admin
from project import views as project_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', project_views.ProjecViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
    #path('projects/', project_views.ProjectListAPIView.as_view()),
    path('projects/<uuid:pk>/', project_views.ProjectDetailAPIView.as_view()),
    path('projects/<uuid:pk>/likes/', project_views.ProjectIncreaseLikesAPIView.as_view()),
]
 