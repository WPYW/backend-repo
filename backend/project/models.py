from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel
)

class Projecct(
    Model, # PK > 이름 : id, 형식 : uuid
    TitleDescriptionModel,
	TimeStampedModel, 
	ActivatorModel,
	):

	class Meta:
		verbose_name = 'Product'
		verbose_name_plural = "Products"
		ordering = ["id"]

	github_link = models.CharField(max_length=200, null=False)
	demo_link = models.CharField(max_length=200)
	views = models.IntegerField(default=0, null=False)
	likes = models.IntegerField(default=0, null=False)

	def __str__(self):
		return f'{self.title}'
