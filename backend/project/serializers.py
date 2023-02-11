from . import models
from rest_framework import serializers
from rest_framework.fields import CharField



class ProjectPostSerializer(serializers.ModelSerializer):
 
	projectTitle = CharField(source="title", required=True)
	projectDescription = CharField(source="description", required=True)
	githubLink = CharField(source="github_link", required=True)
	demositeLink = CharField(source="demo_link")
	
	class Meta:
		model = models.Projecct
		fields = (
			'projectTitle',
			'projectDescription',
			'githubLink',
   			'demositeLink',
			'views',
			'likes',
			'created',
			'modified',
			'status',
			'activate_date',
			'deactivate_date',
		)

