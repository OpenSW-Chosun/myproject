from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.http import JsonResponse

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

# colab api, process_viedo
def process_video(request):
    if request.method == "POST":
        video = request.FILES.get("video")
        model_type = request.POST.get("model_type")

        if not video or not model_type:
            return render(request, 'model_use.html', {"result": "영상과 모델을 선택해주세요."})

        # Colab API URL 설정
        colab_api_url = "https://e0ad-35-187-244-50.ngrok-free.app/api/predict"

        try:
            # Colab API에 파일 전송
            response = requests.post(
                colab_api_url,
                files={"file": video},
                data={"model_type": model_type}
            )
            response.raise_for_status()
            result_data = response.json()
            result = result_data.get("message", "No prediction message.")
        except requests.exceptions.RequestException as e:
            result = f"Colab API 요청 실패: {str(e)}"
        except ValueError:
            result = "Colab API로부터 올바르지 않은 응답이 왔습니다."

        return render(request, 'model_use.html', {"result": result})

    return render(request, 'model_use.html')