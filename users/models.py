from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User, related_name = 'profile', on_delete = models.CASCADE) # 사용자와 1:1 관계 설정
  # on delete=models.CASCADE : 사용자가 삭제될 때 프로필도 함께 삭제됨
  
  # dropdown 선택지 (charfield + choices)
  # 1. 현재 이동 조건
  CONDITION_CHOICES = [
    ('none', '해당 없음'),
    ('wheelchair', '휠체어 이용'),
    ('visual_impaired', '시각 장애'),
    ('leg_fracture', '다리 골절'),
  ]
  movement_condition = models.CharField(max_length = 20, choices = CONDITION_CHOICES, default = 'none')

  # 2. 선호 경로 설정
  # 계단 피하기
  avoid_stairs = models.BooleanField(default = False)
  # 경사 피하기
  avoid_ramps = models.BooleanField(default= False)
  # 엘리베이터 선호
  prefer_elevator = models.BooleanField(default = False)
  
  def __str__(self):
    return f"{self.user.username}의 프로필"
  
