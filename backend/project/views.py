from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ProjectPostSerializer, PreviewImageSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import views, status, generics, viewsets
from rest_framework.response import Response
from .models import Project
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.decorators import parser_classes

# class ProjectPagination(PageNumberPagination):
#     page_size = 5

class ProjecViewSet(viewsets.ModelViewSet):
    queryset  = Project.objects.all()
    serializer_class = ProjectPostSerializer
    # pagination_class = ProjectPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created', 'likes', 'views']
    # 역순정렬 하려면 > http://127.0.0.1:8000/projects?ordering=-likes 이렇게 앞에 -를 붙여야 함

    parser_classes = (MultiPartParser, FormParser)


class ProjectDetailAPIView(views.APIView):
    """
    A simple APIView for creating contact entires.
    """
    
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({"result": "error","message": "Project does not exist"}, status= 400)

    def get(self, request, pk):
        try:
            project = self.get_object(pk)
            project.views += 1
            project.save()
            project_serializer = ProjectPostSerializer(project)
            return Response(project_serializer.data)
        except JSONDecodeError:
                return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)


class ProjectIncreaseLikesAPIView(views.APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({"result": "error","message": "Project does not exist"}, status= 400)
        
    def patch(self, request, pk):
        try:
            project = self.get_object(pk)
            project.likes += 1
            project.save()
            project_serializer = ProjectPostSerializer(project)
            return Response(project_serializer.data)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
