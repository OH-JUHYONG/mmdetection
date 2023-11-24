import os
import shutil
import random


def move_and_split_matching_files(source_dir_json, source_dir_tif, target_dir, train_ratio, val_ratio, test_ratio):
    # .json 파일과 .tif 파일을 찾기
    json_files = [file for file in os.listdir(
        source_dir_json) if file.endswith('.json')]
    tif_files = [file for file in os.listdir(
        source_dir_tif) if file.endswith('.tif')]

    # 파일 이름을 기준으로 매칭
    matching_files = [(json, tif) for json in json_files for tif in tif_files if json.split(
        '.')[0] == tif.split('.')[0]]

    # 파일을 랜덤하게 섞고, 훈련, 검증, 테스트 세트로 나누기
    random.shuffle(matching_files)
    num_files = len(matching_files)
    num_train = int(num_files * train_ratio)
    num_val = int(num_files * val_ratio)

    # 파일 세트별로 분할
    train_files = matching_files[:num_train]
    val_files = matching_files[num_train:num_train + num_val]
    test_files = matching_files[num_train + num_val:]

    # 각 세트의 파일을 타겟 디렉토리의 적절한 서브디렉토리로 이동
    for set_name, files in [('train', train_files), ('val', val_files), ('test', test_files)]:
        images_set_dir = os.path.join(target_dir, 'images', set_name)
        annfiles_set_dir = os.path.join(target_dir, 'annfiles', set_name)
        os.makedirs(images_set_dir, exist_ok=True)
        os.makedirs(annfiles_set_dir, exist_ok=True)

        for json_file, tif_file in files:
            shutil.move(os.path.join(source_dir_json, json_file),
                        os.path.join(annfiles_set_dir, json_file))
            shutil.move(os.path.join(source_dir_tif, tif_file),
                        os.path.join(images_set_dir, tif_file))


# 소스 디렉토리와 타겟 디렉토리 설정
source_dir_json = "D:\\1. Development\\project\\asan\\annfiles"
source_dir_tif = "D:\\1. Development\\project\\asan\\images"
target_dir = "D:\\1. Development\\project\\asan_split"

# 비율 설정
train_ratio = 0.6
val_ratio = 0.2
test_ratio = 0.2

# 함수 호출하여 파일 이동 및 분할
move_and_split_matching_files(
    source_dir_json, source_dir_tif, target_dir, train_ratio, val_ratio, test_ratio)
