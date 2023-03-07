
from datetime import date
from . import models
from rest_framework import serializers
from rest_framework.fields import CharField ,DateField, BooleanField
from django.contrib.auth.hashers import make_password

class  RecruitPostSerializer (serializers.ModelSerializer): 
  recruitTechskill = serializers.SerializerMethodField()
  recruitPosition = serializers.SerializerMethodField()
  recruitTitle = CharField(source="title", required=True)
  recruitDescription = CharField(source="description", required=True)
  recruitType = CharField(source="recruit_type", required=True)
  recruitMember = CharField(source="recruit_member", required=True)
  startDate = DateField(source="recruit_start", required=True)
  endDate = DateField(source="recruit_end", required=True)
  is_remote = BooleanField (required=True)
  deadline = DateField(required=True)
  contact= CharField(source="contact_Info", required=True) 
  password = CharField(required=True, write_only=True)
  shut = BooleanField(required=True)
  class Meta: 
    model = models.Recruit
    fields = (
      'id',
			'recruitTitle', # list에서 comment 안 나오게 하고 싶으면 지우기
      'recruitDescription',
			'recruitType',
			'recruitMember',
      'recruitTechskill',
      'recruitPosition',
			'startDate',
			'endDate',
      'is_remote',
			'deadline',
      'dday',
			'contact',
      'shut',
      'password',
      'views',
      'likes',
      )
    extra_kwargs= {
      'password' : {'write_only' : True},
      'id' : {'read_only': True}
    }
  def get_recruitPosition(self, obj):
    recruit_Position = obj.recruitPosition.all()
    position_serializer = PositionSerializer(instance=recruit_Position, many=True, context=self.context).data
    result_position = []
    for i in position_serializer:
      result_position.append(dict(i).get('position'))
    return result_position
  
  def get_recruitTechskill(self,obj):
    recruitTechskill = obj.recruitTechskill.all()
    techSkill_serializer = TechskillSerializer(instance=recruitTechskill, many=True, context=self.context).data
    result_techSkill = []
    for i in techSkill_serializer: 
      result_techSkill.append(dict(i).get('techSkill'))
    return result_techSkill
  
  def create(self, validated_data): 
  # passwords = validated_data.pop('password',None)
    recruit = models.Recruit.objects.create(**validated_data)
    position = self.context['request'].data
    for position in position.getlist('recruitPosition'):
      get_position = models.Position.objects.filter(title=position)
      if get_position:
        get_position =models.Position.objects.create(title=position)
      models.recruitPosition.objects.create(recruit=recruit,position=get_position)
    recruit.password = make_password(validated_data['password'])
    recruit.save()
    return recruit


class TechskillSerializer(serializers.ModelSerializer):
  
  class Meta: 
      model = models.TechSkill
      fields = (
        'id',
        'techSkill',
        'logo_image',
        'created',
        'modified',
        'status',
        'activate_date',
        'deactivate_date',
      )
class RecruitTechskillSerializer(serializers.ModelSerializer):
  techSkill = serializers.SlugRelatedField(
    slug_field='techSkill',
    read_only=True
  )
  class Meta: 
      model = models.Recruit_Techskill
      fields = (
        # 'id',
        'techSkill',
        'logo_image',
      #   'created',
      #   'modified',
      #   'status',
      #   'activate_date',
			# 'deactivate_date',
      )

class PositionSerializer(serializers.ModelSerializer):
  class Meta: 
    model = models.Position
    fields = (
      'id',
      'position'
      'created',
      'modified',
      'status',
      'activate_date',
			'deactivate_date',
    )

class RecruitPositionSerializer(serializers.ModelSerializer):
  position = serializers.SlugRelatedField(
    slug_field='position',
    read_only=True
  )
  class Meta:
      model = models.Recruit_Position
      fields = (
        # 'id',
        'position'
      #   'created',
      #   'modified',
      #   'status',
      #   'activate_date',
			# 'deacti
      )



class CommentSerializer(serializers.ModelSerializer):

	class Meta: 	
		model = models.RecruitComment
		fields = (
	    	'id',
			'nickname',
			'content',
			'created',
			# 'status',
			# 'activate_date',
			# 'deactivate_date',
		)
