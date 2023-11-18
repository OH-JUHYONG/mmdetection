import sys
custom_imports = dict(
    imports=['mmdet.datasets.asan'],  allow_failed_imports=False)

_base_ = [
    '../_base_/models/mask-rcnn_r50_fpn.py',
    '../_base_/datasets/asan_instance.py',
    '../_base_/schedules/schedule_2x.py', '../_base_/default_runtime.py'
]

model = dict(
    backbone=dict(
        frozen_stages=4,  # 모든 단계 동결
    ),
    roi_head=dict(
        bbox_head=dict(num_classes=10),  # asan시 class 갯수 + 1(background)
        mask_head=dict(num_classes=10)))


# train 할 때 수정해야 하는 부분
data = dict(
    # 단일 GPU에서 한 번에 처리할 수 있는 이미지 개수, 값을 증가시키면 한 epoch를 완료하는 데 걸리는 시간이 단축될 수 있지만, GPU 메모리를 많이 사용
    samples_per_gpu=2,
    # DataLoader가 데이터를 미리 가져오는 데 사용할 수 있는 서브프로세스의 수, 값을 증가시키면 I/O 병목현상을 줄일 수 있음
    workers_per_gpu=4,
)

auto_scale_lr = dict(enable=True, base_batch_size=4)

# test 할 때 수정
test_evaluator = dict(
    # test image들의 test.bbox.json, test.seg.json 파일 저장
    outfile_prefix='./mmd_output/mmd_1116_v1/test'
)

# pretrained weight 사용
load_from = '/home/ohanthony/mmdetection/checkpoints/mask_rcnn_r50_fpn_mstrain-poly_3x_coco_20210524_201154-21b550bb.pth'
