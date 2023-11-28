import sys
custom_imports = dict(
    imports=['mmdet.datasets.asan'],  allow_failed_imports=False)

_base_ = [
    '../_base_/models/mask-rcnn_r50_fpn.py',
    '../_base_/datasets/asan_instance.py',
    '../_base_/schedules/schedule_2x.py', '../_base_/default_runtime.py'
]


# 클래스별 가중치 설정
# 'Vehicle', 'Greenhouse', 'Temporary building', 'Bale silage', 'Tent' 클래스에 높은 가중치
# ex)... 7.77% --> 100 / 7.77 = 12.87
# weights = [6, 13, 5, 3, 18, 15, 22, 23, 10]
# 계산의 편의를 위해 나온 비율에서 최저 값(3)으로 나눔
weights = [1, 5, 1, 1, 6, 5, 7, 7, 3, 1]


model = dict(
    roi_head=dict(
        bbox_head=dict(
            num_classes=9,  # asan시 class 갯수 + 1(background)
            # weight cross entropy 적용
            loss_cls=dict(
                type='CrossEntropyLoss',
                use_sigmoid=False,
                loss_weight=1.0,
                class_weight=weights
            )
        ),
        mask_head=dict(
            num_classes=9
        )
    )
)


# train 할 때 수정해야 하는 부분
data = dict(
    # 단일 GPU에서 한 번에 처리할 수 있는 이미지 개수, 값을 증가시키면 한 epoch를 완료하는 데 걸리는 시간이 단축될 수 있지만, GPU 메모리를 많이 사용
    samples_per_gpu=4,
    # DataLoader가 데이터를 미리 가져오는 데 사용할 수 있는 서브프로세스의 수, 값을 증가시키면 I/O 병목현상을 줄일 수 있음
    workers_per_gpu=4,
)

auto_scale_lr = dict(enable=True, base_batch_size=16)

# test 할 때 수정
test_evaluator = dict(
    # test image들의 test.bbox.json, test.seg.json 파일 저장
    outfile_prefix='./mmd_output/mmd_1126_v3/test'
)

# pretrained weight 사용
load_from = '/home/ohanthony/mmdetection/checkpoints/mask_rcnn_r50_fpn_mstrain-poly_3x_coco_20210524_201154-21b550bb.pth'
# load_from = '/home/ohanthony/mmdetection/work_dirs/mask-rcnn_r50_fpn_1x_asan/1126_v3/epoch_24.pth'
