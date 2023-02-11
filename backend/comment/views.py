from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Comment
from .serializers import CommentSerializer

# Create your views here.
# @api_view(['GET', 'POST'])
# def comment_list(request):
#   if request.method == 'GET':
#     queryset = Comment.objects.all()
#     serializer = CommentSerializer(queryset, many=True )
#     return Response(serializer.data)
#   elif request.method == 'POST':
#     data = JSONParser().parse(request)
#     serializer = CommentSerializer(data = data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentAPIView(views.APIView): 
  def get(self, request): 
    queryset = Comment.objects.all()
    serializer = CommentSerializer(queryset, many=True )
    return Response(serializer.data)
  def post(self, request):
    try:  
      data = JSONParser().parse(request)
      serializer = CommentSerializer(data = data)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
      else: 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)


@api_view(['GET', 'POST', 'DELETE'])
def comment_detail(request, pk):
  try:
    comment = Comment.objects.get (pk=pk)
  except Comment.DoesNotExist:
    return Response(status=status.HTTP_404_BAD_REQUEST)
  if request.method == 'GET':
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = CommentSerializer(comment , data=request.data)
    if serializer.is_valid():
        serializer.save( )
        return Response(serializer.data)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':  
      comment.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
  

class CommentDetailAPIView(views.APIView):
  def comment_detail(request, pk):
    try:
      comment = Comment.objects.get (pk=pk)
    except Comment.DoesNotExist:
      return Response(status=status.HTTP_404_BAD_REQUEST)
  def get(self, request, pk):
      comment = Comment.objects.get (pk=pk)
      serializer = CommentSerializer(comment)
      return Response(serializer.data)
  def put(self, request, pk):
      comment = Comment.objects.get(pk=pk)
      data = JSONParser().parse(request)
      serializer = CommentSerializer(comment , data=data)
      if serializer.is_valid():
        serializer.save( )
        return Response(serializer.data)
      return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
  def delete(self, request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

