import json
import matplotlib.pyplot as plt

# JSON 파일 경로
json_file_path = '/home/ohanthony/mmdetection/work_dirs/mask-rcnn_r50_fpn_ms-poly-3x_coco/20231108_084508/vis_data/scalars.json'

# bbox mAP 및 segm mAP 데이터를 저장할 리스트들
bbox_map_values = {'mAP': [], 'mAP_50': [],
                   'mAP_75': [], 'mAP_s': [], 'mAP_m': [], 'mAP_l': []}
segm_map_values = {'mAP': [], 'mAP_50': [],
                   'mAP_75': [], 'mAP_s': [], 'mAP_m': [], 'mAP_l': []}

# JSON 파일에서 mAP 추출
with open(json_file_path, 'r') as json_file:
    for line in json_file:
        try:
            data = json.loads(line)
            for key in bbox_map_values.keys():
                if f'coco/bbox_{key}' in data:
                    bbox_map_values[key].append(data[f'coco/bbox_{key}'])
            for key in segm_map_values.keys():
                if f'coco/segm_{key}' in data:
                    segm_map_values[key].append(data[f'coco/segm_{key}'])
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")

# bbox mAP 그래프 그리기
plt.figure(figsize=(10, 5))
for key, values in bbox_map_values.items():
    plt.plot(values, label=f'bbox {key}')
plt.title('BBox mAP Metrics Over Time')
plt.xlabel('Epochs')
plt.ylabel('mAP')
plt.legend()
# bbox mAP 그래프 저장
plt.savefig(
    '/home/ohanthony/mmdetection/outputs/show_train_loss/1108_bbox_mAP.png')
plt.show()

# segm mAP 그래프 그리기
plt.figure(figsize=(10, 5))
for key, values in segm_map_values.items():
    plt.plot(values, label=f'segm {key}')
plt.title('Segmentation mAP Metrics Over Time')
plt.xlabel('Epochs')
plt.ylabel('mAP')
plt.legend()
# segm mAP 그래프 저장
plt.savefig(
    '/home/ohanthony/mmdetection/outputs/show_train_loss/1108_seg_mAP.png')
plt.show()
