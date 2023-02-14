from django.urls import include, path
from django.contrib import admin
from project import views as project_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', project_views.ProjecViewSet)
urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('api/v1/admin/', admin.site.urls),
    #path('projects/', project_views.ProjectListAPIView.as_view()),
    #path('api/v1/projects/<uuid:pk>/', project_views.ProjectDetailAPIView.as_view()),
    path('api/v1/projects/<uuid:pk>/likes/', project_views.ProjectIncreaseLikesAPIView.as_view()),
]
 