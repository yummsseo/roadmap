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
# ROADMAP/urls.py

from django.contrib import admin
from django.urls import path, include

# 💡 Simple JWT 뷰 Import
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),
    
    # 💡 [핵심] 로그인(토큰 발급) 및 토큰 갱신 엔드포인트 추가
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 앱별 URL 연결 (users 앱과 roadmap 앱)
    path('api/users/', include('users.urls')),
    path('api/roadmap/', include('roadmap.urls')),
]