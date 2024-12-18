"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
from .views import process_video
from . import views
# from MesoNet_model import xception

def index_view(request):
    return render(request, 'index.html')  # 'index.html' 렌더링

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # 기본 URL에 index 연결
    path('faceforensics/', views.faceforensics, name='faceforensics'),  # FaceForensics 추가
    path('model_types/', views.model_types, name='model_types'),
    path('model_comparison/', views.model_comparison, name='model_comparison'),
    path('model_use/', views.model_use, name='model_use'),
    path('process_video/', views.process_video, name='process_video'),  # 추가된 경로
]