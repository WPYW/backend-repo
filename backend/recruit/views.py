from datetime import date
from json import JSONDecodeError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from recruit.models import Recruit
from .models import Comment
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .serializers import CommentSerializer, RecruitPostSerializer, RecruitPositionSerializer, RecruitTechskillSerializer
from django.contrib.auth.hashers import check_password
import requests
from rest_framework import views, status, generics, viewsets
from django.contrib.auth.hashers import make_password

class RecruitViewSet(viewsets.ModelViewSet):
  queryset  = Recruit.objects.all()
  serializer_class = RecruitPostSerializer
  #어떤것들을 필터링해서 보여줄지, 
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  parser_classes = (MultiPartParser, FormParser)
  search_fields = ['title']
  ordering_fields = ['created','likes','views']
  def get_object(self, pk):
    try:
        return Recruit.objects.get(pk=pk)
    except Recruit.DoesNotExist:
        return JsonResponse({"result": "error","message": "Project does not exist"}, status= 400)
  def retrieve(self,request, pk):
    try: 
      recruit = self.get_object(pk)
      recruit.views += 1
      recruit.save()
      recruit_serializer = RecruitPostSerializer(recruit)
      return Response(recruit_serializer.data)
    except JSONDecodeError: 
      return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
  def update(self ,request ,pk):
    try:
      recruits = self.get_object(pk)
      recruit_serializer = RecruitPostSerializer(recruits, data = request.data)  
      if recruit_serializer.is_valid(raise_exception=True):
        self.perform_update(recruit_serializer)
      return Response(recruit_serializer.data)  
    except JSONDecodeError: 
        return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

  # def put(self, request,pk, *args, **kwargs):
  #   #recruit = self.get_object()
  #   recruit = recruit.objects.get(pk = kwargs['pk'] )
  #   update_serial = RecruitPostSerializer(recruit, data = request.data)
  #   if update_serial.is_valid():
  #     update_serial.save()
  #     return JsonResponse(
  #           update_serial.data, 
  #           status = status.HTTP_201_CREATED, safe=False
  #           )
  #   return JsonResponse(
  #       update_serial.errors, 
  #       status = status.HTTP_400_BAD_REQUEST, safe=False
  #       )
  def delete(self ,request ,pk):
    # try:
    #   recruits = self.get_object(pk)
    #   recruit_serializer = RecruitPostSerializer(recruits, data = request.data)  
    #   if check_password(request.data.__getitem__('password'), recruits.password):
    #     if recruit_serializer.is_valid(raise_exception=True):
    #       self.delete()
    #       return Response(status=status.HTTP_204_NO_CONTENT)
    #   return HttpResponse({'Success':"Deleted Successfully."})  
    # except JSONDecodeError: 
    #   return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
    
    recruit = self.get_object(pk)
    recruit.delete()
        #   return HttpResponse({'Success':"Deleted Successfully."})   


class CommentViewSet(views.APIView): 
    # queryset  = Comment.objects.all()
    # serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)
    def get_object(self, pk):
        try:
            return Recruit.objects.get(pk=pk)
        except Recruit.DoesNotExist:
            return JsonResponse({"result": "error","message": "Project does not exist"}, status= 400) 
    def create_random_nickname(self):
        random_nickname = requests.get("https://nickname.hwanmoo.kr/?format=json").json()
        return random_nickname.get("words")[0]
    def post(self, request, pk):  
        try:
            recruit = self.get_object(pk)
            random_nickname = self.create_random_nickname()
            comment = Comment.objects.create(recruit=recruit, nickname = random_nickname, content=request.data.get("content"))
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
    def get(self, request, pk):  
        try:
            recruit = self.get_object(pk)
            comment = Comment.objects.filter(recruit=recruit)
            comment_serializer = CommentSerializer(comment, many=True)
            return Response(comment_serializer.data)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

