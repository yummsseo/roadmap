"""
URL configuration for roadmap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. 메인 주소 (http://127.0.0.1:8001/)에 접속하면 main 앱으로 연결합니다.
    path('', include('main.urls')), 
    
    # 2. Django 관리자 페이지
    path('admin/', admin.site.urls),
    
    # 3. users 앱 (님의 파일 구조에 따라)
    path('api/users/', include('users.urls')),
    path('api/', include('main.urls')) #추가
    
    # [주의] 만약 main 앱에 API 기능도 구현한다면 이 라인도 살려두세요.
    #path('api/main/', include('main.urls')),
]




