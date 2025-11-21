from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.views.generic import TemplateView # 수정

#def index(request):
#    return render(request, 'map.html') 
class MapPageView(TemplateView):
    template_name = 'main/map.html'




@csrf_exempt  
def get_route(request):
    if request.method == 'POST':
        TMAP_APP_KEY = "HRfwcjIwBt78mOxVBBGYH6MSQKPcv7SzadLC0GXh" 

        try:
            received_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        start_lat = received_data.get('startLat')
        start_lon = received_data.get('startLon')
        end_lat = received_data.get('endLat')
        end_lon = received_data.get('endLon')
        
        if not all([start_lat, start_lon, end_lat, end_lon]):
            return JsonResponse({"error": "Missing coordinates"}, status=400)

        url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"
        headers = {
            "appKey": TMAP_APP_KEY,
            "Content-Type": "application/json"
        }
        
        payload = {
            "startX": start_lon,
            "startY": start_lat,
            "endX": end_lon,
            "endY": end_lat,
            "reqCoordType": "WGS84GEO",
            "resCoordType": "WGS84GEO",
            "startName": "출발지",
            "endName": "도착지"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return JsonResponse({"error": "TMap API Request Failed", "detail": str(e), "status_code": response.status_code}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Network Error", "detail": str(e)}, status=500)


        route_data = response.json()
        path_points = []
        obstacle_points = []
        
        totalDistance = 0
        
        for feature in route_data.get('features', []):
            geometry = feature.get('geometry')
            properties = feature.get('properties')

            if geometry.get('type') == 'Point':
                description = properties.get('description', '')
                facility_type = properties.get('facilityType')
                
                # 횡단보도/건널목 체크 (description 기반)
                if '횡단보도' in description or '건널목' in description:
                    obstacle_points.append({
                        'lon': geometry['coordinates'][0],
                        'lat': geometry['coordinates'][1],
                        'type': '횡단보도',
                    })
                
                # 기존 장애물(facilityType 기반) 체크 (계단, 경사로, 에스컬레이터 등)
                elif facility_type in ['11', '12', '21', '22']:
                    obstacle_points.append({
                        'lon': geometry['coordinates'][0],
                        'lat': geometry['coordinates'][1],
                        'type': description
                    })
            
            elif geometry.get('type') == 'LineString':
                for coord in geometry.get('coordinates', []):
                    path_points.append(coord)
                
                if 'totalDistance' in properties:
                    totalDistance = properties.get('totalDistance', 0)


        return JsonResponse({
            "path": path_points,
            "obstacles": obstacle_points,
            "distance": totalDistance,
            "time": properties.get('totalTime', 0)
        })
    
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)