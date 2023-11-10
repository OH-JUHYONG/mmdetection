import json
import matplotlib.pyplot as plt

# JSON 파일 경로
json_file_path = '/home/ohanthony/mmdetection/work_dirs/mask-rcnn_r50_fpn_ms-poly-3x_coco/20231108_084508/vis_data/scalars.json'

# 로스 데이터를 저장할 리스트
losses = []

# JSON 파일에서 로스 추출
with open(json_file_path, 'r') as json_file:
    for line in json_file:
        try:
            data = json.loads(line)
            if 'loss' in data:
                losses.append(data['loss'])
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")

# 그래프 그리기
plt.figure(figsize=(10, 5))
plt.plot(losses, label='Loss')
plt.title('Training Loss')
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.legend()

# 그래프를 이미지 파일로 저장하기
# PNG 형식으로 저장
plt.savefig(
    '/home/ohanthony/mmdetection/outputs/show_train_loss/1108_train_loss.png')

plt.show()
