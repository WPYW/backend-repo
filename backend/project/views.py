from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ProjectPostSerializer, PreviewImageSerializer , CommentSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import views, status, generics, viewsets
from rest_framework.response import Response
from .models import Project, Comment
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
    
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({"result": "error","message": "Project does not exist"}, status= 400)

    def retrieve(self, request, pk):
        try:
            project = self.get_object(pk)
            project.views += 1
            project.save()
            project_serializer = ProjectPostSerializer(project)
            return Response(project_serializer.data)
        except JSONDecodeError:
                return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)


# class ProjectDetailAPIView(views.APIView):
#     """
#     A simple APIView for creating contact entires.
#     """
    
#     def get_object(self, pk):
#         try:
#             return Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             return JsonResponse({"result": "error","message": "Project does not exist"}, status= 400)

#     def retrieve(self, request, pk):
#         try:
#             project = self.get_object(pk)
#             project.views += 1
#             project.save()
#             project_serializer = ProjectPostSerializer(project)
#             return Response(project_serializer.data)
#         except JSONDecodeError:
#                 return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)


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


class CommentViewSet(views.APIView): 
    parser_classes = (MultiPartParser, FormParser)
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({"result": "error","message": "Project does not exist"}, status= 400)

    def post(self, request, pk):  
        project = self.get_object(pk)
        comment = Comment.objects.create(project=project, content=request.data.get("content"))
        #serializer = CommentSerializer(data = request.data)
        return JsonResponse({"success":"ok"},status = status.HTTP_201_CREATED)

        #if serializer.is_valid():   
        #    serializer.save()
        #    return JsonResponse(serializer.data,status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status = status.HTTP_400_CREATED)        
