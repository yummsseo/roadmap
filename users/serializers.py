from django.contrib.auth.models import User #Django 내장 기본 user 모델
from django.contrib.auth.password_validation import validate_password #비밀번호 유효성 검사기
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserCreationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
  email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset = User.objects.all())])

  class Meta:
    model = User
    fields = ['username', 'email', 'password']
    #회원가입이 이름,이메일,비밀번호 받음

  def create(self, validated_data):
    # 장고 기본 유저 모델의 create_user 메서드 사용해 비밀번호 해시화하여 저장
    user = User.objects.create_user(
      username =validated_data['username'],
      email = validated_data['email'],
      password = validated_data['password']
    )
    return user