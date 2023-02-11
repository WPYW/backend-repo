from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ProjectPostSerializer
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from .models import Projecct



class ProjectAPIView(views.APIView):
    """
    A simple APIView for creating contact entires.
    """
    def get(self, request):
        projects = Projecct.objects.all()
        projects_serializer = ProjectPostSerializer(projects, many=True)
        return Response(projects_serializer.data)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = ProjectPostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
