_base_ = [
    # '../common/ms-poly_3x_coco-instance.py', 해당 파일이 있는 경우 중복키 문제 발생
    '../_base_/models/mask-rcnn_r50_fpn.py',

    # Insatnce segmentation을 이용한 mask r-cnn을 사용하기 때문
    '../_base_/datasets/coco_instance.py',
    '../_base_/schedules/schedule_2x.py',  # coco 데이터셋 기준으로 12 epoch 동안의 학습
    '../_base_/default_runtime.py'
]


dataset_root = '/home/ohanthony/mmdetection/data/asan'

# 변형한 coco labeling 형식에 맞게 classes 설정
classes = ('Water', 'Vehicle', 'Road', 'Farmland', 'Greenhouse',
           'Temporary building', 'Bale silage', 'Tent', 'Trash')

# 재개할 체크포인트 파일 경로 추가, 따로 커맨드 명령어에 --resume-from 할 필요 없어짐
resume_from = '/home/ohanthony/checkpoints/mask_rcnn_r50_fpn_mstrain-poly_3x_coco_20210524_201154-21b550bb.pth'


# Runner 설정에 auto_scale_lr을 추가
# runner = dict(
#     type='EpochBasedRunner',
#     max_epochs=12,  # 12 epochs
#     auto_scale_lr=dict(enable=True)  # 원래 사용된 배치 사이즈로 설정
# )


# dataset 경로 설정
data = dict(
    # 단일 GPU에서 한 번에 처리할 수 있는 이미지 개수, 값을 증가시키면 한 epoch를 완료하는 데 걸리는 시간이 단축될 수 있지만, GPU 메모리를 많이 사용
    samples_per_gpu=8,
    # DataLoader가 데이터를 미리 가져오는 데 사용할 수 있는 서브프로세스의 수, 값을 증가시키면 I/O 병목현상을 줄일 수 있음
    workers_per_gpu=4,
    train=dict(
        img_prefix=dataset_root + 'train_images/',
        classes=classes,
        ann_file=dataset_root + 'annotations/train.json'
    ),
    val=dict(
        img_prefix=dataset_root + 'val_images/',
        classes=classes,
        ann_file=dataset_root + 'annotations/val.json'
    ),
    test=dict(
        img_prefix=dataset_root + 'test_images/',
        classes=classes,
        ann_file=dataset_root + 'annotations/test.json'
    )
)
