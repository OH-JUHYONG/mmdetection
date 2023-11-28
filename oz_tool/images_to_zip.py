import os
import zipfile

# 경로 설정
path = "C:\\Users\\ohanthony\\Desktop\\Capstone Design 2023-2\\Data\\1차 시흥"

# 지정된 경로에서 .tif 확장자를 가진 파일들만 추출
tif_files = [f for f in os.listdir(path) if f.endswith('.tif')]

# .zip 파일 생성 및 .tif 파일 추가
with zipfile.ZipFile('tif_files.zip', 'w') as zipf:
    for file in tif_files:
        zipf.write(os.path.join(path, file), arcname=file)

# .zip 파일 경로 확인
zip_file_path = os.path.abspath('tif_files.zip')
print(zip_file_path)
