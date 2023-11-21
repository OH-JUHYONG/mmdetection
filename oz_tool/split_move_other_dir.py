import os
import shutil
import random


def move_files_except_random(src_dir_annotations, src_dir_images, dst_dir_annotations, dst_dir_images, num_to_keep):
    # 어노테이션 파일과 이미지 파일의 이름 목록을 가져옵니다 (확장자 제외)
    annotation_files = [os.path.splitext(f)[0] for f in os.listdir(
        src_dir_annotations) if f.endswith('.json')]
    image_files = [os.path.splitext(f)[0] for f in os.listdir(
        src_dir_images) if f.endswith('.tif')]

    # 공통 파일 이름 찾기
    common_files = set(annotation_files).intersection(image_files)

    # 무작위로 선택된 파일을 제외한 나머지 파일을 이동시킵니다
    common_files = list(common_files)
    random.shuffle(common_files)
    files_to_move = common_files[num_to_keep:]

    for file in files_to_move:
        # 어노테이션 파일 이동
        src_annotation_path = os.path.join(src_dir_annotations, file + '.json')
        dst_annotation_path = os.path.join(dst_dir_annotations, file + '.json')
        shutil.move(src_annotation_path, dst_annotation_path)

        # 이미지 파일 이동
        src_image_path = os.path.join(src_dir_images, file + '.tif')
        dst_image_path = os.path.join(dst_dir_images, file + '.tif')
        shutil.move(src_image_path, dst_image_path)


# 설정
src_annotations = "/home/ohanthony/datasets/asan/annfiles/test/"
src_images = "/home/ohanthony/datasets/asan/images/test/"
dst_annotations = "/home/ohanthony/datasets/asan/annfiles/train/"
dst_images = "/home/ohanthony/datasets/asan/images/train/"
num_to_keep = 10  # src 디렉토리에 남길 파일 수

# 실행
move_files_except_random(src_annotations, src_images,
                         dst_annotations, dst_images, num_to_keep)
