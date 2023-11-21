import os
import shutil
import random


def copy_and_split_json_files(source_dir, target_dir, copy_ratio, train_ratio, val_ratio, test_ratio):
    # 원본 디렉토리 내의 모든 JSON 파일 가져오기
    all_json_files = [os.path.join(root, file) for root, dirs, files in os.walk(
        os.path.join(source_dir, "annfiles")) for file in files if file.endswith('.json')]

    # 복사할 파일 수 계산
    num_to_copy = int(len(all_json_files) * copy_ratio)

    # 랜덤하게 JSON 파일 선택
    random_json_files = random.sample(all_json_files, num_to_copy)

    # 파일을 Train, Val, Test로 나누어 저장
    num_train = int(num_to_copy * train_ratio)
    num_val = int(num_to_copy * val_ratio)

    train_files = random_json_files[:num_train]
    val_files = random_json_files[num_train:num_train+num_val]
    test_files = random_json_files[num_train+num_val:]

    # 디렉토리 생성 및 파일 복사
    for dest, files in [("train", train_files), ("val", val_files), ("test", test_files)]:
        dest_dir = os.path.join(target_dir, dest)
        os.makedirs(dest_dir, exist_ok=True)
        for source_file_path in files:
            file_name = os.path.basename(source_file_path)
            target_file_path = os.path.join(dest_dir, file_name)
            shutil.copy2(source_file_path, target_file_path)

    print(f"JSON 파일 데이터셋 분할 및 복사가 완료되었습니다.")

    return random_json_files  # 수정된 부분: random_json_files를 반환


def copy_and_split_image_files(source_dir, target_dir, json_files, train_ratio, val_ratio, test_ratio):
    image_source_dir = os.path.join(source_dir, "images")
    image_target_dir = os.path.join(target_dir, "images")

    # JSON 파일과 동일한 이름의 TIF 파일 찾기
    tif_files = []
    for json_file in json_files:
        json_file_name = os.path.basename(json_file)
        tif_file_name = os.path.splitext(json_file_name)[0] + ".tif"
        tif_file_path = find_tif_file(image_source_dir, tif_file_name)
        if tif_file_path:
            tif_files.append(tif_file_path)

    if not tif_files:
        print("TIF 파일을 찾을 수 없습니다.")
        return

    # 파일을 Train, Val, Test로 나누어 저장
    num_to_copy = len(tif_files)
    num_train = int(num_to_copy * train_ratio)
    num_val = int(num_to_copy * val_ratio)

    train_files = tif_files[:num_train]
    val_files = tif_files[num_train:num_train+num_val]
    test_files = tif_files[num_train+num_val:]

    # 디렉토리 생성 및 파일 복사
    for dest, files in [("train", train_files), ("val", val_files), ("test", test_files)]:
        dest_dir = os.path.join(image_target_dir, dest)
        os.makedirs(dest_dir, exist_ok=True)
        for source_file_path in files:
            file_name = os.path.basename(source_file_path)
            target_file_path = os.path.join(dest_dir, file_name)
            shutil.copy2(source_file_path, target_file_path)

    print(f"TIF 파일 데이터셋 분할 및 복사가 완료되었습니다.")


def find_tif_file(directory, tif_file_name):
    for root, dirs, files in os.walk(directory):
        if tif_file_name in files:
            return os.path.join(root, tif_file_name)
    return None


# 원본 디렉토리와 목표 디렉토리 경로 설정
source_dir = "D:\\1. Development\\project\\asan"  # 원본 디렉토리 경로
target_dir = "D:\\1. Development\\project\\asan_split"  # 복사할 파일을 저장할 새로운 디렉토리 경로

# 비율 설정
copy_ratio = 1
train_ratio = 0.9
val_ratio = 0.05
test_ratio = 0.05

# annfiles 디렉토리의 JSON 파일 복사 및 분할
json_target_dir = os.path.join(target_dir, "annfiles")
os.makedirs(json_target_dir, exist_ok=True)
json_files = copy_and_split_json_files(
    source_dir, json_target_dir, copy_ratio, train_ratio, val_ratio, test_ratio)

# annfiles 디렉토리의 JSON 파일과 동일한 이름의 TIF 파일 복사 및 분할
copy_and_split_image_files(source_dir, target_dir,
                           json_files, train_ratio, val_ratio, test_ratio)
