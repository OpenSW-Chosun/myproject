import os
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# 모델 스크립트 import (환경에 맞게 경로 수정)
from MesoNet_model import mesonet
#from faceforensics.xception_model import XceptionModel  # 수정된 경로
# from MesoNet_model import efficientnet
import io
import base64
import matplotlib.pyplot as plt

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

COLAB_SERVER_URL = 'https://7f38-34-125-111-96.ngrok-free.app/api/predict'

def process_video(request):
    if request.method == 'POST':
        # 모델 유형 및 업로드된 비디오 파일 가져오기
        model_type = request.POST.get('model_type')
        video_file = request.FILES.get('video')

        if not video_file:
            return render(request, 'model_use.html', {'result': '비디오 파일이 업로드되지 않았습니다.'})

        # 비디오 파일을 서버에 임시 저장
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        video_path = fs.save(video_file.name, video_file)
        full_video_path = os.path.join(settings.MEDIA_ROOT, video_path)

        result = None  # 결과를 저장할 변수

        try:
            # 모델에 따라 로컬 또는 Colab API에서 처리
            if model_type == 'mesonet':
                # MesoNet 예측 수행
                frame_predictions = mesonet.predict(full_video_path)  # 프레임별 예측 결과 리스트 반환
                
                # 디버깅: frame_predictions 내용 확인
                print("frame_predictions (before filtering):", frame_predictions)

                # 숫자(float)만 필터링
                frame_predictions = [float(pred) for pred in frame_predictions if is_number(pred)]

                # 딥페이크 판별 계산
                total_frames = len(frame_predictions)
                deepfake_detected = sum(1 for pred in frame_predictions if pred > 0.5)
                accuracy = deepfake_detected / total_frames if total_frames > 0 else 0

                # 딥페이크 여부 판별
                if accuracy > 0.5:
                    result = f"이 영상은 딥페이크로 판별되었습니다. (딥페이크 확률: {accuracy:.2f})"
                else:
                    result = f"이 영상은 진짜로 판별되었습니다. (딥페이크 확률: {accuracy:.2f})"

            elif model_type == 'faceforensics':
                result = faceforensics.predict(full_video_path)  # 로컬 실행
            elif model_type == 'ensemble':
                result = call_colab_api(full_video_path, model_type)  # Colab API 호출
            else:
                result = '알 수 없는 모델 유형입니다.'
        except Exception as e:
            result = f"오류 발생: {str(e)}"
        finally:
            # 처리 후 서버에 저장된 비디오 파일 삭제
            if os.path.exists(full_video_path):
                os.remove(full_video_path)

        # 결과값을 템플릿으로 전달
        return render(request, 'model_use.html', {'result': result})

    # GET 요청일 경우 페이지 렌더링
    return render(request, 'model_use.html')


def is_number(value):
    """문자열이 숫자인지 확인"""
    try:
        float(value)
        return True
    except ValueError:
        return False

def call_colab_api(video_path, model_type):
    """
    Colab 서버에 비디오 파일과 모델 유형을 전송하여 결과를 반환하는 함수
    """
    try:
        with open(video_path, 'rb') as f:
            files = {'file': f}
            data = {'model_type': model_type}
            response = requests.post(COLAB_SERVER_URL, files=files, data=data)

        if response.status_code == 200:
            return response.json().get('message', '결과를 가져올 수 없습니다.')
        else:
            return f"Colab 서버 에러: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Colab 서버 요청 중 오류 발생: {str(e)}"

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
