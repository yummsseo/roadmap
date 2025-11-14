from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserCreationSerializer
from rest_framework.permissions import AllowAny #누구나 접근 허용

class SignupView(views.APIView):
  permission_classes = [AllowAny] #누구나 접근 허용

  def post(self, request):
    serializer = UserCreationSerializer(data = request.data)
    if serializer.is_valid():
      user = serializer.save()
      login(request,user) #회원가입 후 자동 로그인
      return Response({"message": "회원가입 성공"}, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
  
class LoginView(views.APIView):
  permission_classes = [AllowAny] #누구나 접근 허용

  def post(self,request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
      return Response({"error" : '아이디와 비밀번호를 모두 입력해주세요.'}, status = status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username = username, password = password)
    if user is not None:
      login(request, user)
      return Response({'message' : f'{user.username}님, 환영합니다!'}, status = status.HTTP_200_OK)
    else:
      return Response({'error' : '아이디 또는 비밀번호가 올바르지 않습니다.'}, status = status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(views.APIView):
  def post(self,request):
    logout(request)
    return Response({'message' : '로그아웃되었습니다.'}, status = status.HTTP_200_OK)
