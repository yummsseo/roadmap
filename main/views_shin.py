import requests
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import Settingser, Notifyser
from .models import Setting, Notify
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.conf import settings

# class MapPageView(TemplateView):
#     template_name = 'main/map.html'

# class RouteSearchView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         start_text = request.data.get('start')
#         end_text = request.data.get('end')
        
#         if not start_text or not end_text:
#             return Response({"error": "출발지와 도착지를 모두 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
#         api_key = settings.TMAP_API_KEY

#         # 🔑 API 키 확인 (디버깅용)
#         print(f"🔑 API Key 로드 확인: {api_key[:10] if api_key else 'None'}...")
        
#         if not api_key or api_key == 'FALLBACK_KEY_FOR_TESTING': 
#             print("🚨 TMAP API Key가 로드되지 않았습니다!")
#             return Response({"error": "API 키 로드 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         try:
#             # 텍스트를 좌표로 변환
#             start_coord = self.get_coordinates(api_key, start_text)
#             end_coord = self.get_coordinates(api_key, end_text)
            
#             if not start_coord or not end_coord:
#                 return Response({
#                     "error": "장소를 찾을 수 없습니다. 정확한 주소나 장소로 입력해주세요."
#                 }, status=status.HTTP_404_NOT_FOUND)
            
#             # 사용자 설정 확인
#             try:
#                 user_setting = Setting.objects.get(user=request.user)
#             except Setting.DoesNotExist:
#                 user_setting = None

#             # 경로 옵션 설정
#             search_option = "0"  # 기본값
#             if user_setting:
#                 if (user_setting.wheelchair_user or user_setting.leg_injury_user or 
#                     user_setting.senior_user or user_setting.no_stair):
#                     search_option = "30"  # 계단 제외
            
#             # TMAP 보행자 경로 API 호출
#             url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json'
            
#             payload = {
#                 "startX": start_coord['lon'],
#                 "startY": start_coord['lat'],
#                 "endX": end_coord['lon'],
#                 "endY": end_coord['lat'],
#                 "reqCoordType": "WGS84GEO",
#                 "resCoordType": "WGS84GEO",
#                 "startName": start_text,
#                 "endName": end_text,
#                 "searchOption": search_option
#             }
            
#             headers = {
#                 "appKey": api_key,
#                 "Content-Type": "application/json"
#             }
            
#             print(f"🚀 경로 검색 요청: {start_text} → {end_text}")
#             response = requests.post(url, json=payload, headers=headers)
            
#             print(f"📡 경로 API 응답 코드: {response.status_code}")
            
#             if response.status_code == 200:
#                 return Response(response.json(), status=status.HTTP_200_OK)
#             else:
#                 print(f"🚨 경로 API 실패: {response.text}")
#                 return Response({
#                     "error": "TMAP API 호출 실패",
#                     "details": response.text
#                 }, status=response.status_code)
                
#         except Exception as e:
#             print(f"🚨 예외 발생: {str(e)}")
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
#     def get_coordinates(self, api_key, keyword):
#         """주소/키워드를 좌표로 변환 (POI 검색)"""
        
#         # 방법 1: 헤더에 appKey (기본)
#         url = 'https://apis.openapi.sk.com/tmap/pois?version=1&format=json'
        
#         params = {
#             "searchKeyword": keyword,
#             "resCoordType": "WGS84GEO",
#             "reqCoordType": "WGS84GEO",
#             "count": 1
#         }
        
#         headers = {
#             "appKey": api_key,
#             "Accept": "application/json"
#         }
        
#         print(f"🔍 POI 검색: {keyword}")
#         response = requests.get(url, params=params, headers=headers)
        
#         print(f"📡 POI API 응답 코드: {response.status_code}")
        
#         # 401 에러 시 대안 방법 시도
#         if response.status_code == 401:
#             print("⚠️ 헤더 방식 실패, URL 파라미터 방식 시도...")
            
#             # 방법 2: URL 파라미터에 appKey
#             params['appKey'] = api_key
#             response = requests.get(url, params=params)
#             print(f"📡 대안 방식 응답 코드: {response.status_code}")
        
#         if response.status_code != 200:
#             print(f"🚨 POI API 호출 실패, Status Code: {response.status_code}")
#             print(f"🚨 응답 내용: {response.text}")
#             return None
        
#         try:
#             data = response.json()
            
#             if "searchPoiInfo" in data and "pois" in data['searchPoiInfo']:
#                 pois = data["searchPoiInfo"]["pois"]["poi"]
#                 if pois and len(pois) > 0:
#                     poi = pois[0]
#                     coords = {
#                         "lat": poi["noorLat"],
#                         "lon": poi["noorLon"]
#                     }
#                     print(f"✅ 좌표 찾음: {coords}")
#                     return coords
            
#             print(f"⚠️ POI 결과 없음: {keyword}")
#             return None
            
#         except Exception as e:
#             print(f"🚨 JSON 파싱 에러: {str(e)}")
#             return None




# 출발지,도착지 구현 (지도 렌더링)
class MapPageView(TemplateView):
    template_name = 'main/map.html'

class RouteSearchView(APIView):
    permission_classes = [IsAuthenticated] # 로그인한 사용자만 길찾기 가능

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
            
        serializer = Settingser(instance=instance, data=request.data)
        if serializer.is_valid():
            setting_ob = serializer.save(user=request.user)
            return Response(
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
#수정부분

# 건의사항
from rest_framework.generics import ListCreateAPIView

class Notifyv(ListCreateAPIView):
    serializer_class = Notifyser
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        locationtext = serializer.validated_data.get('location')
        latitude = None
        longitude = None

        TMAP_KEY = settings.TMAP_API_KEY
        
        if locationtext:
            try:
                url = "https://apis.openapi.sk.com/tmap/geo/fullAddrGeocoding"
                params = {
                    "version": "1",
                    "fullAddr": locationtext,
                    "appKey": TMAP_KEY
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                coordinate_data = data.get('coordinateInfo', {}).get('coordinate', [])
                
                if coordinate_data:
                    longitude = float(coordinate_data[0].get('lon')) 
                    latitude = float(coordinate_data[0].get('lat'))
                    
            except requests.RequestException as e:
                print(f"TMap API 호출 실패: {e}")

        serializer.validated_data['latitude'] = latitude
        serializer.validated_data['longitude'] = longitude
        serializer.save()