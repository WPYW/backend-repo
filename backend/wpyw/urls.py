from django.urls import include, path
from django.contrib import admin
from project import views as project_views
from rest_framework import routers
from recruit import views as recruit_views

router = routers.DefaultRouter()
router.register(r'projects', project_views.ProjecViewSet)
# router.register(r'projects/<uuid:pk>/comments', project_views.CommentViewSet)
router.register(r'recruits', recruit_views.RecruitViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('api/v1/admin/', admin.site.urls),
    #path('projects/', project_views.ProjectListAPIView.as_view()),
    #path('api/v1/projects/<uuid:pk>/', project_views.ProjectDetailAPIView.as_view()),
    path('api/v1/projects/<uuid:pk>/likes/', project_views.ProjectIncreaseLikesAPIView.as_view()),
    path('api/v1/projects/<uuid:pk>/comments/', project_views.CommentViewSet.as_view()), # 
    #path('api/v1/recruits/<uuid:pk>/dday/',)
    # path('api/v1/recruits/<uuid:pk>/likes/', recruit_views.RecruitIncreaseAPIView.as_view()), # 
    path('api/v1/recruits/<uuid:pk>/comments/', recruit_views.CommentViewSet.as_view()), # 
    
]
