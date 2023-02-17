from . import models
from rest_framework import serializers
from rest_framework.fields import CharField
from pathlib import Path
import os
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
	projectHashtag = serializers.SerializerMethodField()
	comment = serializers.SerializerMethodField()
	projectTitle = CharField(source="title", required=True)
	projectDescription = CharField(source="description", required=True)
	githubLink = CharField(source="github_link", required=True)
	demositeLink = CharField(source="demo_link")
	
	class Meta:
		model = models.Project
		fields = (
	        'id',
					'comment',
        	'previewImages',
			'projectHashtag',
			'projectTitle',
			'projectDescription',
			'githubLink',
   			'demositeLink',
			'views',
			'likes',
			'created',
			# 'modified',
			# 'status',
			# 'activate_date',
			# 'deactivate_date',
		)

	def get_previewImages(self, obj):
		image = obj.previewImages.all() 
		preview_image_serializer = PreviewImageSerializer(instance=image, many=True, context=self.context).data
		result_preview_image = []
		for i in preview_image_serializer:
			result_preview_image.append(dict(i).get('previewImages'))
		return result_preview_image

	def get_projectHashtag(self, obj):
		project_hashtag = obj.projectHashtag.all()
		project_hashtag_serializer = ProjectHashtagSerializer(instance=project_hashtag, many=True, context=self.context).data
		result_hashtag = []
		for i in project_hashtag_serializer:
			result_hashtag.append(dict(i).get('hashtag'))
		return result_hashtag
	
	def get_comment(self, obj):
		comment = obj.comment.all()
		
		comment_serializer = CommentSerializer(instance=comment, many=True, context=self.context).data
		# result_hashtag = []
		# for i in project_hashtag_serializer:
		# 	result_hashtag.append(dict(i).get('hashtag'))
		return comment_serializer
    
	def create(self, validated_data):
		project = models.Project.objects.create(**validated_data)
		images_data = self.context['request'].FILES
		for image_data in images_data.getlist('previewImages'):
			# 파일 이름 바꾸는 방법
   			# path_etc = image_data.name.split('.')[-1]
			# image_data.name = f'{project.id}/abc.{path_etc}'
			models.Preview_Image.objects.create(project=project, image_url=image_data)
		hashtag = self.context['request'].data
		for hashtag in hashtag.getlist('projectHashtag'):
			get_hashtag = models.Hashtag.objects.filter(title=hashtag)
			if get_hashtag:
				get_hashtag = models.Hashtag.objects.get(title=hashtag)
				get_hashtag.count += 1
				get_hashtag.save()
			else:
				get_hashtag = models.Hashtag.objects.create(title=hashtag)
			models.Project_Hashtag.objects.create(project=project, hashtag=get_hashtag)
		return project
	# def create_comment(self, project):
	# 		comment = self.context['request'].data
	# 		post_comment = models.Comment.objects.create()
	# 		models.Project_Comment.objects.creaete(project=project comment=post_comment)

class HashtagSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Hashtag
		fields = (
	        'id',
        	'title',
			'description',
			'created',
			'modified',
			'status',
			'activate_date',
			'deactivate_date',
		)


class ProjectHashtagSerializer(serializers.ModelSerializer):
	# hashtag = HashtagSerializer(read_only=True)
	# hashtag = serializers.StringRelatedField(read_only=True)
	hashtag = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
     )
 
	class Meta:
		model = models.Project_Hashtag
		fields = (
	        # 'id',
			'hashtag',
			# 'created',
			# 'modified',
			# 'status',
			# 'activate_date',
			# 'deactivate_date',
		)
	
class CommentSerializer(serializers.ModelSerializer):

	class Meta: 	
		model = models.Comment
		fields = (
	    'id',
			'content',
			'created',
			'status',
			'created',
			'activate_date',
			'deactivate_date',
		)
