from django.http import HttpResponse
from django.shortcuts import render

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
