from django.conf import settings
from django.shortcuts import redirect
import requests
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Setting, Notify
from .serializers import Settingser, Notifyser
from django.contrib.auth.models import User
from django.db import IntegrityError


# 출발지,도착지 구현 (지도 렌더링)
class MapPageView(TemplateView):
    template_name = 'main/map.html'

    #context 데이터를 템플릿에 전달
    #####??
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # GET 요청에서 'start'와 'end' 쿼리 파라미터를 가져와 컨텍스트에 저장
        context['start_key'] = self.request.GET.get('start', '')
        context['end_key'] = self.request.GET.get('end', '')
        
        return context
#############

class RouteSearchView(APIView):
    permission_classes = [IsAuthenticated] # 로그인한 사용자만 길찾기 가능
    #리다이렉션 추가
    def get(self, request):
        start_key = request.GET.get('start', '')
        end_key = request.GET.get('end', '')
        
        # 'api/map/' 경로로 리다이렉트하면서 쿼리 파라미터를 전달
        return redirect(f'/api/map/?start={start_key}&end={end_key}')
    #추가
    def post(self, request):
        start_text = request.data.get('start')
        end_text = request.data.get('end')
        
        if not start_text or not end_text:
            return Response({"error": "출발지와 도착지를 모두 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = settings.TMAP_API_KEY
        
        if not api_key: 
            return Response({"error": "API 키 로드 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # 텍스트를 좌표로 변환 (Geocoding)
            start_coord = self.get_coordinates(api_key, start_text)
            end_coord = self.get_coordinates(api_key, end_text)
            
            if not start_coord or not end_coord:
                return Response({"error" : "장소를 찾을 수 없습니다. 정확한 주소나 장소로 입력해주세요."}, status=status.HTTP_404_NOT_FOUND)
            
            # 사용자 설정 확인
            try:
                user_setting = Setting.objects.get(user=request.user)
            except Setting.DoesNotExist:
                user_setting = None 

            # TMAP 보행자 경로 옵션 (searchOption = "30" 계단 제외 로직)
            search_option = "0" 
            if user_setting:
                if (user_setting.wheelchair_user or user_setting.leg_injury_user or 
                    user_setting.senior_user or user_setting.no_stair):
                    search_option = "30" 
            
            # TMAP 길찾기 API 호출
            url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json'
            
            payload = {
                "startX" : start_coord['lon'],
                "startY" : start_coord['lat'],
                "endX" : end_coord['lon'],
                "endY" : end_coord['lat'],
                "reqCoordType" : "WGS84GEO",
                "resCoordType" : "WGS84GEO",
                "startName" : start_text,
                "endName" : end_text,
                "searchOption" : search_option
            }
            headers = {
                "appKey" : api_key,
                "Content-Type": "application/json" # POST 요청 시 Content-Type 헤더 필요
            }
            response = requests.post(url, json=payload, headers = headers)

            # 결과 반환
            if response.status_code == 200:
                # TMAP GeoJSON 응답을 프론트엔드로 그대로 전달
                return Response(response.json(), status=status.HTTP_200_OK) 
            else:
                return Response({
                    "error" : "TMAP API 호출 실패",
                    "details": response.text
                }, status = response.status_code)
                
        except Exception as e:
            return Response({"error" : str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
    def get_coordinates(self, api_key, keyword):
        """주소/키워드를 좌표로 변환 (POI 검색)"""
        url = 'https://apis.openapi.sk.com/tmap/pois?version=1&format=json'
        
        params = {
            "searchKeyword" : keyword,
            "resCoordType" : "WGS84GEO",
            "reqCoordType" : "WGS84GEO",
            "count" : 1
        }
        headers = {
            "appKey": api_key
        }
        
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            return None # 401 Unauthorized 에러 등을 밖으로 전달
        
        try:
            data = response.json()
            if "searchPoiInfo" in data and "pois" in data['searchPoiInfo']:
                poi = data["searchPoiInfo"]["pois"]["poi"][0]
                return {
                    "lat" : poi["noorLat"],
                    "lon" : poi["noorLon"]
                }
            return None
        except Exception:
            return None

# 설정 관리
class Settingv(APIView):
    permission_classes = [IsAuthenticated]

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
        setting_obj, created = Setting.objects.get_or_create(user=request.user)
        serializer = Settingser(setting_obj)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

# 건의
class Notifyv(ListCreateAPIView):
    queryset = Notify.objects.all()
    serializer_class = Notifyser
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        locationtext = serializer.validated_data.get('location')
        latitude = None
        longitude = None

        TMAP_API_KEY = settings.TMAP_API_KEY
        if locationtext:
            try:
                url = "https://apis.openapi.sk.com/tmap/geo/fullAddrGeo"
                headers = {"Accept": "application/json", "appKey": TMAP_API_KEY }
                params={
                    "version": "1",
                    "format": "json",
                    "callback": "result",
                    "coordType": "WGS84GEO", # 표준 GPS 좌표계
                    "fullAddr": locationtext
                }
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data: dict = response.json()
                coordinate_info = data.get('coordinateInfo', {})
                coordinate = coordinate_info.get('coordinate', [])
                if coordinate and len(coordinate) > 0:
                    firstcoord = coordinate[0]
                    longitude = float(firstcoord.get('newLon', firstcoord.get('lon', 0))) 
                    latitude = float(firstcoord.get('newLat', firstcoord.get('lat', 0)))

            except requests.RequestException as e:
                print(f"TMap API 호출 실패 : {e}")

        serializer.save(latitude=latitude, longitude=longitude)
