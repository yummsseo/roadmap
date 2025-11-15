from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import SignupForm

# Create your views here.
# main/views.py

def signup(request):
    if request.method == 'POST':
        # (POST 로직)
        ...
        return redirect('home')
    else: # <--- GET 요청일 때 이 부분이 없으면 에러가 납니다
        form = SignupForm()
    
    # GET 요청이거나 POST에서 폼이 유효하지 않을 때
    return render(request, 'main/signup.html', {'form': form}) # <--- 이 return이 최종적으로 실행되어야 합니다.

def login_page(request):
    if request.method == 'POST':
        # (POST 로직)
        ...
        return redirect('home')
    else: # <--- GET 요청일 때 이 부분이 없으면 에러가 납니다
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form}) # <--- 이 return이 최종적으로 실행되어야 합니다.