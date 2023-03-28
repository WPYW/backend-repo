from django.db import models
from utils.model_abstracts import Model
from enum import Enum
from django.contrib.auth.hashers import make_password
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel
)


class Recruit(
  Model,
  TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
):
  class Meta: 
    verbose_name = 'Recruit'
    verbose_name_plural = "Recruits"
    ordering =  ["-created"]
  member = models.IntegerField( null = False)
  deadline = models.DateField(null = False)
  contact_Info = models.CharField(max_length=200, null=False)
  shut = models.BooleanField(null = False)
  password = models.CharField(max_length=200,null = False)
  views = models.IntegerField(default=0, null=False)
  likes = models.IntegerField(default=0,null=False)
  # recruit_title = title 
  # recruit_ descript = description 
  def __str__(self):
    return f'{self.id}'


class Techskill(
  Model,
  TimeStampedModel, 
	ActivatorModel,
):
  class Meta:
    verbose_name = 'Techskill'
    verbose_name_plural = "Techskills"
    ordering = ["created"]
  #   recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
  techskill = models.CharField(max_length=200, null=False, default=" ")
  def __str__(self):
    return f'{self.techskill}'


class Recruit_Techskill(
  Model,
  TimeStampedModel, 
	ActivatorModel,
  ):
  class Meta:
    verbose_name = 'Recruit_Techskill'
    verbose_name_plural = "Recruit_Techskills"
    ordering = ["created"]
  recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name='recruitTechskill')
  techskill = models.ForeignKey(Techskill, on_delete=models.CASCADE,related_name='Techskill')
  def __str__(self):
    return f'{self.id}'


class PositionTypes(Enum):
  frontend = 'frontend'
  backend = 'backend'
  design  = 'design'
  mobile  = 'mobile'
  devops = 'devops'
  

class Position(
  Model,
  TimeStampedModel, 
	ActivatorModel,
):
  class Meta:
    verbose_name = 'Position'
    verbose_name_plural = "Positions"
    ordering = ["created"]
  position = models.CharField(default='',max_length=50, null=False)
  def __str__(self):
      return f'{self.position}'

class Recruit_Position(
  Model,
  TimeStampedModel, 
	ActivatorModel,
):
  class Meta:
    verbose_name = 'Recruit_Position'
    verbose_name_plural = "Recruit_Positions"
    ordering = ["created"]
  recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name='recruitPosition')
  position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='positions')
  def __str__(self):
    return f'{self.id}'
  


class Comment(
  Model,
  TimeStampedModel,
  ActivatorModel,
) : 
  class Meta: 
    verbose_name = 'Comment'
    verbose_name_plural = "Comment"
    ordering = ['-created']
  nickname = models.CharField(max_length=200, null=False)
  recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name='comment')
  content = models.CharField( max_length=200, null=False)
  def __str__(self):
    return f'{self.id}'