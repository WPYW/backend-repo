
from datetime import date
from . import models
from rest_framework import serializers
from rest_framework.fields import CharField ,DateField, BooleanField
from django.contrib.auth.hashers import make_password

class  RecruitPostSerializer (serializers.ModelSerializer): 
  recruitTechskill = serializers.SerializerMethodField()
  recruitPosition = serializers.SerializerMethodField()
  title = CharField(required=True)
  description = CharField( required=True)
  types = CharField( required=True)
  member = CharField(required=True)
  startDate = DateField(source="start", required=True)
  endDate = DateField(source="end", required=True)
  is_remote = BooleanField (required=True)
  deadline = DateField(required=True)
  contact= CharField(source="contact_Info", required=True) 
  password = CharField(required=True, write_only=True)
  shut = BooleanField(required=True)
  comment = serializers.SerializerMethodField()
  class Meta: 
    model = models.Recruit
    fields = (
      'id',
			'title', # list에서 comment 안 나오게 하고 싶으면 지우기
      'description',
			'types',
			'member',
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
      'comment'
      )
    extra_kwargs= {
      'password' : {'write_only' : True},
      'id' : {'read_only': True}
    }
  def get_recruitPosition(self, obj):
    recruit_Position = obj.recruitPosition.all()
    recruit_position_serializer = PositionSerializer(instance=recruit_Position, many=True, context=self.context).data
    result_position = []
    for i in recruit_position_serializer:
      result_position.append(dict(i).get('position'))
    return result_position
  
  def get_recruitTechskill(self,obj):
    recruitTechskill = obj.recruitTechskill.all()
    techskill_serializer = TechskillSerializer(instance=recruitTechskill, many=True, context=self.context).data
    result_techskill = []
    for i in techskill_serializer: 
      result_techskill.append(dict(i).get('techskill'))
    return result_techskill
  
  def get_comment(self, obj):
    comment = obj.comment.all()
    comment_serializer = CommentSerializer(instance=comment, many=True, context=self.context).data
    return comment_serializer
    
  def create(self, validated_data): 
  # passwords = validated_data.pop('password',None)
    recruit = models.Recruit.objects.create(**validated_data)
    position = self.context['request'].data
    techskill = self.context['request'].data
    for position in position.getlist('recruitPosition'):
      get_position = models.Position.objects.filter(position=position)
      if get_position:
        get_position = models.Position.objects.get(position=position)
      else:
        get_position =models.Position.objects.create(position=position)
      models.Recruit_Position.objects.create(recruit=recruit,position=get_position)
    for techskill in techskill.getlist('recruitTechskill'):
      get_Techskill = models.Techskill.objects.filter(techskill=techskill)
      if get_Techskill:
        get_Techskill = models.Techskill.objects.get(techskill=techskill)
      else:
        get_Techskill= models.Techskill.objects.create(techskill=techskill)
    models.Recruit_Techskill.objects.create(recruit=recruit,techskill=get_Techskill)
    recruit.password = make_password(validated_data['password'])
    Dday = recruit.deadline - date.today()
    recruit.dday = Dday.days
    recruit.save()
    return recruit
  
  # def update(self, instance,  validated_data):

  #   instance.title = validated_data('title', instance.title)
  #   instance.description = validated_data('description', instance.description)    
  #   instance.types = validated_data('types', instance.types)
  #   instance.member = validated_data('member', instance.member)
  #   instance.recruitTechskill = validated_data('recruitTechskill', instance.recruitTechskill)
  #   instance.recruitPosition = validated_data('recruitPosition', instance.recruitPosition)
  #   instance.startDate = validated_data('startDate', instance.startDate)
  #   instance.endDate = validated_data('endDate', instance.endDate)
  #   instance.is_remote= validated_data('is_remote', instance.is_remote)
  #   instance.deadline = validated_data('deadline', instance.deadline)
  #   instance.contact = validated_data('contact ', instance.contact)
  #   instance.shut = validated_data('shut', instance.shut)
  #   print(instance)
  #   instance.save()

class RecruitPutSerializer (serializers.ModelSerializer):
  class Meta: 
    model = models.Recruit
    fields =(
      
    )
    
class TechskillSerializer(serializers.ModelSerializer):
  
  class Meta: 
      model = models.Techskill
      fields = (
        'id',
        'techskill',
        'created',
        'modified',
        'status',
        'activate_date',
        'deactivate_date',
      )
      
class RecruitTechskillSerializer(serializers.ModelSerializer):
  techskill = serializers.SlugRelatedField(
    slug_field='techSkill',
    read_only=True
  )
  class Meta: 
      model = models.Recruit_Techskill
      fields = (
        # 'id',
        'techskill',
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
      'position',
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
		model = models.Comment
		fields = (
	    'id',
			'nickname',
			'content',
			'created',
			# 'status',
			# 'activate_date',
			# 'deactivate_date',
		)

