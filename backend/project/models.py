from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel
)

class Project(
    Model, # PK > 이름 : id, 형식 : uuid
    TitleDescriptionModel,
	TimeStampedModel, 
	ActivatorModel,
	):

	class Meta:
		verbose_name = 'Project'
		verbose_name_plural = "Projects"
		ordering = ["-created"]

	github_link = models.CharField(max_length=200, null=False)
	demo_link = models.CharField(max_length=200)
	views = models.IntegerField(default=0, null=False)
	likes = models.IntegerField(default=0, null=False)

	def __str__(self):
		return f'{self.title}'

class Preview_Image(
	Model, # PK > 이름 : id, 형식 : uuid
	TimeStampedModel, 
	ActivatorModel,
	):
    
	class Meta:
		verbose_name = 'PreviewImage'
		verbose_name_plural = "PreviewImages"
		ordering = ["created"]
	
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='previewImages')
	image_url = models.ImageField(null=False)
	
	def __str__(self):
		return f'{self.id}'
