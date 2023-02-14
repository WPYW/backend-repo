from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel
)
from django.conf import settings
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
		return f'{self.id}'

def get_img_storage_path(instance, filename):
	return 'project/images/%s/%s' % (instance.project.pk, filename)

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
	image_url = models.ImageField(upload_to=get_img_storage_path, null=False)
	
	def __str__(self):
		return f'{self.project}'
	

class Hashtag(
	Model, # PK > 이름 : id, 형식 : uuid
	TitleDescriptionModel,
	TimeStampedModel, 
	ActivatorModel,
	):
    
	class Meta:
		verbose_name = 'Hashtag'
		verbose_name_plural = "Hashtag"
		ordering = ["created"]

	count = models.IntegerField(default=1, null=False)	
 
	def __str__(self):
		return f'{self.title}({self.count})'

class Project_Hashtag(
	Model, # PK > 이름 : id, 형식 : uuid
	TimeStampedModel, 
	ActivatorModel,
	):
    
	class Meta:
		verbose_name = 'Project_Hashtag'
		verbose_name_plural = "Project_Hashtag"
		ordering = ["created"]
	
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectHashtag')
	hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='hashtag')
	
	def __str__(self):
		return f'{self.id}'
