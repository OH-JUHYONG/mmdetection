import os

def limit_files_to_match(directory1, ext1, directory2, ext2, limit):
    files1 = {f.split('.')[0] for f in os.listdir(directory1) if f.endswith(ext1)}
    files2 = {f.split('.')[0] for f in os.listdir(directory2) if f.endswith(ext2)}

    # 교집합을 찾아서 정렬
    common_files = sorted(list(files1.intersection(files2)))

    # 제한 수보다 많으면 앞에서부터 제한 수만큼 잘라내기
    if len(common_files) > limit:
        common_files = common_files[:limit]

    # 두 디렉토리에서 필요없는 파일 삭제
    for directory, ext, files in [(directory1, ext1, files1), (directory2, ext2, files2)]:
        for file in files:
            if file not in common_files:
                os.remove(os.path.join(directory, file + ext))

# 파일 경로 설정
images_test_dir = "/home/ohanthony/datasets/asan/dataset_v8/images/train/"
annfiles_test_dir = "/home/ohanthony/datasets/asan/dataset_v8/annfiles/train/"

# 파일 제한 함수 호출
limit_files_to_match(images_test_dir, '.tif', annfiles_test_dir, '.json', 110000)
