from django.http import JsonResponse
from django.shortcuts import render
from recruit.models import Recruit
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .serializers import RecruitPostSerializer, RecruitPositionSerializer, RecruitTechskillSerializer

# Create your views here.


class RecruitViewSet(viewsets.ModelViewSet):
  queryset  = Recruit.objects.all()
  serializer_class = RecruitPostSerializer
  #어떤것들을 필터링해서 보여줄지, 
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  parser_classes = (MultiPartParser, FormParser)
  #search_fields = ['title','position','techskill']
  ordering_fields = ['created','likes','views']
  # def get_object(self, pk):
  #   try:
  #       return Recruit.objects.get(pk=pk)
  #   except Recruit.DoesNotExist:
  #       return JsonResponse({"result": "error","message": "Project does not exist"}, status= 400)

  # def post(self, pk, request):
  #     recruit = self.get_object(pk)
  #     serializer = RecruitPostSerializer(data=request.data)
  #     if serializer.is_valid():
  #         serializer.save()
  #         return JsonResponse(serializer.data, status=201)
  #     return JsonResponse(serializer.errors, status=400)     
  