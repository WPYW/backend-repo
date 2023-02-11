from . import models
from rest_framework import serializers
from rest_framework.fields import CharField


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
      model = models.Comment
      fields = '__all__'