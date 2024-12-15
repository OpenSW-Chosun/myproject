import os
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
# from .utils import process_video_with_colab  # Colab 통신 함수 임포트


# 모델 스크립트 import (환경에 맞게 경로 수정)
from MesoNet_model import mesonet
#from faceforensics.xception_model import XceptionModel  # 수정된 경로
# from MesoNet_model import efficientnet

# COLAB_SERVER_URL = 'https://5466-34-90-50-63.ngrok-free.app/api/predict'  # Colab Flask 서버 URL로 변경 필요

# 인덱스 페이지
def index(request):
    return render(request, 'index.html')

# FaceForensics 페이지
def faceforensics(request):
    return render(request, 'faceforensics.html')

# 모델 종류 페이지
def model_types(request):
    return render(request, 'model_type.html')

# 모델 비교 페이지
def model_comparison(request):
    return render(request, 'model_comparison.html')

# 모델 사용 페이지
def model_use(request):
    return render(request, "model_use.html")



COLAB_SERVER_URL = 'https://https://4742-34-90-50-63.ngrok-free.app/api/predict'

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
        elif model_type == 'faceforensics':
           result = faceforensics.predict(full_video_path)  # faceforensics 사용
        # elif model_type == 'efficientnet':
        #     result = efficientnet.predict(full_video_path)
        else:
            result = '알 수 없는 모델 유형입니다.'
        
        # 처리 후 파일 삭제(선택사항)
        os.remove(full_video_path)

        # 결과를 템플릿으로 전달
        return render(request, 'model_use.html', {'result': result})
    
    # GET 요청일 경우 단순히 페이지 보여줌(또는 redirect)
    return redirect('model_use.html')  # 혹은 model_use.html 로직에 맞게 수정

# ------------------------------------------------------------------------------colab api
# def process_video(request):
#     if request.method == 'POST':
#         # 모델 유형 및 업로드된 파일 가져오기
#         model_type = request.POST.get('model_type')
#         video_file = request.FILES.get('video')

#         if not video_file:
#             return render(request, 'model_use.html', {'result': '비디오 파일이 업로드되지 않았습니다.'})

#         # 비디오 파일을 서버에 임시 저장 (MEDIA_ROOT 경로)
#         fs = FileSystemStorage(location=settings.MEDIA_ROOT)
#         video_path = fs.save(video_file.name, video_file)
#         full_video_path = os.path.join(settings.MEDIA_ROOT, video_path)

#         try:
#             # Colab 서버로 비디오 파일 및 모델 유형 전송
#             with open(full_video_path, 'rb') as f:
#                 files = {'file': f}
#                 data = {'model_type': model_type}
#                 response = requests.post(COLAB_SERVER_URL, files=files, data=data)

#             if response.status_code == 200:
#                 # Colab 서버에서 받은 결과 메시지
#                 result = response.json().get('message', '결과를 가져올 수 없습니다.')
#             else:
#                 result = f"Colab 서버 에러: {response.status_code}"

#         except requests.exceptions.RequestException as e:
#             result = f"Colab 서버 요청 중 오류 발생: {str(e)}"

#         finally:
#             # (선택사항) 처리 후 서버에 저장된 비디오 파일 삭제
#             os.remove(full_video_path)

#         # 결과를 템플릿으로 전달
#         return render(request, 'model_use.html', {'result': result})

#     # GET 요청일 경우 단순히 페이지를 렌더링
#     return render(request, 'model_use.html')


#-------------------------------------------------------------------------- 준언 실험 파일 
# COLAB_SERVER_URL = 'https://https://4742-34-90-50-63.ngrok-free.app/api/predict'

# def process_video_with_colab(video_path, model_type):
#     try:
#         # 비디오 파일과 모델 유형을 Colab 서버로 전송
#         with open(video_path, 'rb') as f:
#             files = {'video': f}
#             data = {'model_type': model_type}
#             response = requests.post(COLAB_SERVER_URL, files=files, data=data)

#         if response.status_code == 200:
#             # Colab 서버의 결과 반환
#             return response.json().get('result', '결과를 가져올 수 없습니다.')
#         else:
#             return f"Colab 서버 오류: {response.status_code} - {response.text}"

#     except requests.exceptions.RequestException as e:
#         return f"Colab 요청 중 오류 발생: {str(e)}"
    
# # Colab ngrok URL (Colab 실행 후 출력된 URL로 변경)


# def process_video(request):
#     if request.method == 'POST':
#         # 클라이언트로부터 모델 유형과 비디오 파일 받기
#         model_type = request.POST.get('model_type')
#         video_file = request.FILES.get('video')

#         if not video_file:
#             return render(request, 'model_use.html', {'result': '비디오 파일이 업로드되지 않았습니다.'})

#         # 업로드된 비디오 파일 임시 저장
#         fs = FileSystemStorage()
#         video_path = fs.save(video_file.name, video_file)
#         full_video_path = os.path.join(fs.location, video_path)

#         try:
#             # process_video_with_colab 함수 호출
#             result = process_video_with_colab(full_video_path, model_type)
#         finally:
#             # 임시 저장된 파일 삭제
#             if os.path.exists(full_video_path):
#                 os.remove(full_video_path)

#         # 결과 반환
#         return render(request, 'model_use.html', {'result': result})

#     # GET 요청 처리
#     return render(request, 'model_use.html')
