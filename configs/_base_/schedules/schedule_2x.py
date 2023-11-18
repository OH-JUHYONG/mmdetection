# training schedule for 2x
# 학습 과정의 설정 담당, 매 epoch 마다 val_interval = 1을 수행
train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=24, val_interval=1)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

# learning rate
# param_scheduler: 학습률 스케줄러 설정, 학습 동안 학습률을 어떻게 조정할지 정의
# start_factor: 처음 시작할때 학습률, end가지 선형적으로 증가시키는 스케줄러
# by_epoch = False --> 선형적인 증가가 iteration 기반을 의미
# MultiStepLR: milestones에 지정된 epoch에서 학습률을 원래 학습률의 gamma 비율로 감소시킴
param_scheduler = [
    dict(
        type='LinearLR', start_factor=0.001, by_epoch=False, begin=0, end=500),
    dict(
        type='MultiStepLR',
        begin=0,
        end=24,
        by_epoch=True,
        milestones=[16, 22],
        gamma=0.1)
]

# optimizer
optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001))

# Default setting for scaling LR automatically
#   - `enable` means enable scaling LR automatically
#       or not by default.
#   - `base_batch_size` = (8 GPUs) x (2 samples per GPU).
auto_scale_lr = dict(enable=False, base_batch_size=16)
