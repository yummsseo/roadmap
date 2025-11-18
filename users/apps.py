from django.apps import AppConfig
#회원가입 일어나는 순간 userprofile 생성하기 위해 자동화 코드 signals.py 등록

class UsersConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'users'

  def ready(self):
    import users.signals #signals.py를 import하여 신호 수신기 등록