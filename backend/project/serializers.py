from . import models
from rest_framework import serializers
from rest_framework.fields import CharField

class PreviewImageSerializer(serializers.ModelSerializer):
	previewImages = serializers.ImageField(use_url=True, source="image_url", required=True)
	class Meta:
		model = models.Preview_Image
		fields = (
	        'id',
        	'project',
			'previewImages',
			'created',
			'modified',
			'status',
			'activate_date',
			'deactivate_date',
		)

class ProjectPostSerializer(serializers.ModelSerializer):
	
	previewImages = serializers.SerializerMethodField()
	projectTitle = CharField(source="title", required=True)
	projectDescription = CharField(source="description", required=True)
	githubLink = CharField(source="github_link", required=True)
	demositeLink = CharField(source="demo_link")
	
 
	class Meta:
		model = models.Project
		fields = (
	        'id',
        	'previewImages',
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
  
	def get_previewImages(self, obj):
		image = obj.previewImages.all() 
		return PreviewImageSerializer(instance=image, many=True, context=self.context).data
    
	def create(self, validated_data):
		project = models.Project.objects.create(**validated_data)
		images_data = self.context['request'].FILES
		for image_data in images_data.getlist('previewImages'):
			models.Preview_Image.objects.create(project=project, image_url=image_data)
		return project

