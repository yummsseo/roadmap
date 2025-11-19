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
            'blind_user', 
            'leg_injury_user', 
            'senior_user', 
            'no_stair', 
            'no_slopes', 
            'yes_elevator', 
            'yes_escalator',
            'update_at',
        ]
        read_only_fields = ['update_at']

#건의
class Notifyser(serializers.ModelSerializer):
    class Meta:
        model = Notify
        fields = [
            'location', 
            'description',
            'latitude',
            'longitude'
            ]
