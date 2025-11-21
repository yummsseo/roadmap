from rest_framework import serializers
from .models import Setting, Notify
from django.contrib.auth.models import User

#설정
class Settingser(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    useremail = serializers.EmailField(source='user.email',read_only=True)

    class Meta:
        model = Setting
        fields = [
            'username',
            'useremail',
            'wheelchair_user', 
            'leg_injury_user', 
            'senior_user', 
            'no_stair', 
            'no_slopes', 
            'yes_elevator', 
            'yes_escalator',
            'update_at',
        ]
        read_only_fields = ['update_at']
    def update(self, instance, validated_data):   # 검증된 데이터를 반영하고 저장
            for attr, value in validated_data.items():  # 모든 필드(True/False 값)를 기존 객체에 반영
                setattr(instance, attr, value)
        
            instance.save()
            return instance 
#건의
class Notifyser(serializers.ModelSerializer):
    class Meta:
        model = Notify
        fields = [
            'location', 
            'description',
            'latitude',
            'longitude',
            ]
        read_only_fields = ['latitude', 'longitude']