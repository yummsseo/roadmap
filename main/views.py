import requests
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import Settingser, Notifyser
from .models import Setting, Notify
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.conf import settings

# 설정
class Settingv(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):        
        try:
            instance = Setting.objects.get(user=request.user)
        except Setting.DoesNotExist:
            instance = None
        serializer = Settingser(instance=instance,data=request.data)
        if serializer.is_valid():
            setting_ob = serializer.save(user=request.user)
            
            return Response (
                {'status': 'success', 'data': serializer.data}, 
                status=status.HTTP_200_OK
            )
        return Response(
            {'status': 'error', 'errors': serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'status': 'error', 'message': '로그인이 필요합니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            setting_ob = Setting.objects.get(user=request.user)
            serializer = Settingser(setting_ob)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Setting.DoesNotExist:
            return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
        
# 신고
class Notifyv(ListCreateAPIView):
    serializer_class = Notifyser
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        locationtext = serializer.validated_data.get('location')
        latitude = None
        longitude = None

        TMAP_KEY = settings.TMAP_APP_KEY
        if locationtext:
            try:
                url = "https://apis.openapi.sk.com/tmap/geo/fullAddrGeocoding"
                response = requests.get(url, params={
                    "version": "1",
                    "fullAddr": locationtext,
                    "appKey": TMAP_KEY
                })
                response.raise_for_status()
                data: dict = response.json()
                coordinate_data = data.get('coordinateInfo', {}).get('coordinate', [])
                if coordinate_data:
                    longitude = float(coordinate_data[0].get('lon')) 
                    latitude = float(coordinate_data[0].get('lat'))
            except requests.RequestException as e:
                print(f"TMap API 호출 실패 : {e}")

        serializer.validated_data['latitude'] = latitude
        serializer.validated_data['longitude'] = longitude
        serializer.save()