from .models import Users
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        
        user = Users.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            nickname = validated_data['nickname'],
            birthday = validated_data['birthday'],
            thumbail_image_url = validated_data['thumbail_image_url'],
            social = validated_data['social'],
        )
        
        return user


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh_token'])
        data = {'access_token': str(refresh.access_token)}

        return data
