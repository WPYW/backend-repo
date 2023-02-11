from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel
)
# Create your models here.
class Comment(models.Model):
  user = models.CharField(max_length=200, null=False, default="익명")
  message = models.TextField()
  created_At= models.DateTimeField(auto_now_add=True)
  updated_At= models.DateTimeField(auto_now=True)


