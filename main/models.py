from django.db import models
from django.contrib.auth.models import User

# --- 1. 건의/피드백 모델 ---
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

# --- 2. 사용자 설정 모델 (ROU-3, ROU-4 입력값) ---
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

# --- 3. 편의시설 데이터베이스 모델 (ROU-4의 구현 핵심) ---
class Facility(models.Model):
    # 이 모델에 공공 데이터의 엘리베이터, 화장실 위치 정보가 저장됩니다.
    
    TYPE_CHOICES = [
        ('ELEVATOR', '엘리베이터'),
        ('RAMP', '경사로'),
        ('TOILET', '장애인 화장실'),
        ('SHELTER', '쉼터'),
        ('BLIND_WALK', '시각장애인 유도블록'),
    ]

    # 시설 이름 (예: 강남역 엘리베이터)
    name = models.CharField(max_length=255) 
    
    # 시설 종류 (검색 및 필터링에 사용)
    facility_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    
    # 위치 정보
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    # 운영 상태 (예: 고장 여부 등)
    is_operational = models.BooleanField(default=True)
    
    # 외부 데이터 고유 ID (중복 방지)
    external_id = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.get_facility_type_display()})'