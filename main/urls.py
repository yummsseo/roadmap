from django.urls import path
from .views import Settingv, Notifyv

urlpatterns = [
    path('setting/', Settingv.as_view(),name='user_setting'),
    path('notify/',Notifyv.as_view(),name='user_notify')
 ]