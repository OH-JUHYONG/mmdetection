import json
import matplotlib.pyplot as plt

# JSON 파일 경로
json_file_path = '/home/ohanthony/mmdetection/work_dirs/mask-rcnn_r50_fpn_1x_asan/1117_2/vis_data/scalars.json'

# 손실 데이터를 저장할 리스트
losses = []
loss_cls_values = []  # 분류기(classifier)의 손실
loss_bbox_values = []  # Bounding box의 회귀 손실
loss_mask_values = []  # Mask 예측 손실, 객체의 형태를 픽셀 단위로 얼마나 잘 분리하는지 나타냄

# JSON 파일에서 loss_cls 및 loss_bbox 추출
with open(json_file_path, 'r') as json_file:
    for line in json_file:
        try:
            data = json.loads(line)
            # 'loss_cls'와 'loss_bbox' 값이 있는지 확인하고 리스트에 추가
            if 'loss' in data and 'loss_cls' in data and 'loss_bbox' in data and 'loss_mask' in data:
                losses.append(data['loss'])
                loss_cls_values.append(data['loss_cls'])
                loss_bbox_values.append(data['loss_bbox'])
                loss_mask_values.append(data['loss_mask'])
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")

# 그래프 생성
plt.figure(figsize=(10, 5))
plt.plot(losses, label='Loss')
plt.plot(loss_cls_values, label='Loss CLS')
plt.plot(loss_bbox_values, label='Loss BBOX')
plt.plot(loss_mask_values, label='loss_maks')
plt.title('Loss CLS vs Loss BBOX')
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.legend()

# 그래프를 이미지 파일로 저장,
plt.savefig(
    '/home/ohanthony/mmdetection/mmd_output/mmd_1117_v2/plot/mmd_1117_loss_cls_bbox.png')
plt.show()
