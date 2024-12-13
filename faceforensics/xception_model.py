import torch
from torchvision import transforms
from PIL import Image
import cv2
from torchvision import models

# Xception 모델 클래스 정의
class XceptionModel:
    def __init__(self, model_path="xception-b5690688.pth"):
        # Xception 모델 아키텍처 정의
        self.model = models.xception(pretrained=False)  # Xception 모델 아키텍처 초기화
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))  # 상태 사전 로드
        self.model.eval()  # 평가 모드로 설정

    def predict(self, video_path):
        # 비디오에서 첫 번째 프레임 추출
        frame = self._extract_first_frame(video_path)

        # 이미지를 텐서로 변환
        preprocess = transforms.Compose([
            transforms.Resize((299, 299)),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])
        input_tensor = preprocess(frame).unsqueeze(0)  # 배치 차원 추가

        # 예측 실행
        with torch.no_grad():
            output = self.model(input_tensor)
            _, prediction = torch.max(output, 1)

        # 결과 반환
        return "딥페이크" if prediction.item() == 1 else "정상 비디오"

    def _extract_first_frame(self, video_path):
        video = cv2.VideoCapture(video_path)
        success, frame = video.read()
        video.release()
        if not success:
            raise ValueError("비디오 프레임을 추출할 수 없습니다.")
        return Image.fromarray(frame)