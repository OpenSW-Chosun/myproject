from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.http import JsonResponse
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
# 모델 스크립트 import (환경에 맞게 경로 수정)
from MesoNet_model import mesonet
# from MesoNet_model import xception
# from MesoNet_model import efficientnet

# 인덱스 페이지
def index(request):
    return render(request, 'index.html')

# 모델 종류 페이지
def model_types(request):
    return HttpResponse("This is the model types page.")

# 모델 비교 페이지
def model_comparison(request):
    return HttpResponse("This is the model comparison page.")

# 모델 사용 페이지
def model_use(request):
    return render(request, "model_use.html")


def process_video(request):
    if request.method == 'POST':
        model_type = request.POST.get('model_type')
        video_file = request.FILES.get('video')
        
        if not video_file:
            return render(request, 'model_use.html', {'result': '비디오 파일이 업로드되지 않았습니다.'})
        
        # 업로드한 비디오를 서버 내 임시 저장 (MEDIA_ROOT 경로)
        fs = FileSystemStorage()
        video_path = fs.save(video_file.name, video_file)
        full_video_path = os.path.join(settings.MEDIA_ROOT, video_path)
        
        # 모델 유형에 따라 다른 predict 함수 호출
        if model_type == 'mesonet':
            result = mesonet.predict(full_video_path)
        # elif model_type == 'xception':
        #     result = xception.predict(full_video_path)
        # elif model_type == 'efficientnet':
        #     result = efficientnet.predict(full_video_path)
        else:
            result = '알 수 없는 모델 유형입니다.'
        
        # 처리 후 파일 삭제(선택사항)
        # os.remove(full_video_path)

        # 결과를 템플릿으로 전달
        return render(request, 'model_use.html', {'result': result})
    
    # GET 요청일 경우 단순히 페이지 보여줌(또는 redirect)
    return redirect('model_use.html')  # 혹은 model_use.html 로직에 맞게 수정