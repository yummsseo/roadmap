from django.db import models
from django.contrib.auth.models import User

#신고
class Notify(models.Model):
    #장소 설명
    location = models.CharField(max_length=100, null=True, blank=True)
    #상세 설명
    description = models.TextField(unique=True)
    #위도 
    latitude = models.FloatField(null=True,blank=True)
    #경도
    longitude = models.FloatField(null=True,blank=True)

    def __str__(self):
        return f"{self.location if self.location else '장소 미입력'}" 

# 대시보드 설정
class Setting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #이동 조건
    wheelchair_user = models.BooleanField(default=False)
    blind_user = models.BooleanField(default=False)
    leg_injury_user = models.BooleanField(default=False)
    senior_user = models.BooleanField(default=False)
 
    #선호 경로
    no_stair = models.BooleanField(default=False)
    no_slopes = models.BooleanField(default=False)
    yes_elevator = models.BooleanField(default=False)
    yes_escalator = models.BooleanField(default=False)

    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}의 설정"