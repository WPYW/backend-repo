from django.db import models
from utils.model_abstracts import Model
from enum import Enum
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel
)

class Types(Enum):
  study = "study"
  project = "project"

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
  recruit_type = models.CharField(max_length=10, null = False, choices=[(tag, tag.value) for tag in Types])
  recruit_member = models.IntegerField( null = False)
  recruit_start  = models.DateField(null = False)
  recruit_end  = models.DateField(null = False)
  deadline = models.DateField(null = False)
  contact_Info = models.CharField(max_length=200, null=False)
  shut = models.BooleanField(null = False)
  is_remote = models.BooleanField(null = False)
  password = models.CharField(max_length=200,null = False)
  # recruit_title = title 
  # recruit_ descript = description 
  def __str__(self):
    return f'{self.id}'


class TechSkill(
  Model,
  TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
):
  class Meta:
    verbose_name = 'TechSKill'
    verbose_name_plural = "TechSkills"
    ordering = ["created"]
  #   recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
  #   techskill = models.CharField(max_length=200, null=False)
  def __str__(self):
    return f'{self.title}'


class Recruit_Techskill(
  Model,
  TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
  ):
  class Meta:
    verbose_name = 'Recruit_Techskill'
    verbose_name_plural = "Recruit_Techskills"
    ordering = ["created"]
  recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name='recruitTechskill')
  techskill = models.ForeignKey(TechSkill, on_delete=models.CASCADE,related_name='TechSkill')
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
    verbose_name = 'TechSKill'
    verbose_name_plural = "TechSkills"
    ordering = ["created"]
  position = models.CharField(max_length=200, null = False,choices=[(tag, tag.value) for tag in PositionTypes] )    
  def __str__(self):
      return f'({self.positon})'

class Recruit_Position(
  Model,
  TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
):
  class Meta:
    verbose_name = 'Recruit_Position'
    verbose_name_plural = "Recruit_Positions"
    ordering = ["created"]
  recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name='recruitPosition')
  position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='positions')
  def __str__(self):
    return f'{self.id}'