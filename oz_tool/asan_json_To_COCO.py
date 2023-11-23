import math
import os
import json
from PIL import Image


class To_CocoDataset():
    def __init__(self, img_dir, label_dir, transform=None):
        self.image_dir = img_dir
        self.label_dir = label_dir
        self.transform = transform

        self.dataset = {}
        # 데이터 정보, 라이센스 내용 추가
        self.dataset["info"] = ({"description": "Capston Dataset", "url": "", "version": "1.0",
                                "year": "2023", "contributor": "KwakSeongDae", "date_created": "2023/10"})
        self.dataset["licenses"] = (
            {"url": "https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=realm&dataSetSn=71387", "id": 1, "name": "파나시아"})

        # 이미지 파일 목록을 생성합니다.
        self.image_filenames = [filename for filename in os.listdir(
            img_dir) if filename.endswith('.tif')]

        # JSON 라벨링 파일들을 읽어옴, 딕셔너리로 저장
        self.labels = {}
        for filename in os.listdir(label_dir):
            if filename.endswith('.json'):
                with open(os.path.join(label_dir, filename), 'r', encoding='utf-8') as f:
                    label_data = json.load(f)
                    self.labels[filename] = label_data
        ImagesData = []
        AnnotationsData = []

        # image_no에 해당하는 파일이름을 기반해서 파일을 불러오는 작업
        image_no = 0
        anno_no = 0
        for image_filename in self.image_filenames:
            image_path = os.path.join(self.image_dir, image_filename)
            image = Image.open(image_path)

            # 이미지 파일과 같은 이름의 라벨 value가져옴 + idx증가
            json_file_name = os.path.splitext(image_filename)[0]+".json"
            if self.labels.__contains__(json_file_name):
                label_json = self.labels[json_file_name]  # 확장자명 분리
                image_no += 1
            else:
                continue  # 이미지는 있지만 라벨이 없는 경우에는 제외됨

            # 이미지 정보 추가
            ImagesData.append({"file_name": image_filename,
                              "height": image.size[1], "width": image.size[0], "id": image_no})

            # 라벨링 정보를 cocoDataset에 맞게 가공
            for annotation in label_json['Annotation']:
                # Points에서 x와 y 각각 가장 작은, 큰 좌표를 찾아 Bounding Box 좌표 생성
                points = []
                points.append(annotation['points'][0::2])
                points.append(annotation['points'][1::2])
                x_min = min(points[0])
                y_min = min(points[1])
                x_max = max(points[0])
                y_max = max(points[1])
                # Bounding Box의 좌표 및 크기 계산 -> 원점은 좌상단 꼭지점
                x_center = x_min
                y_center = y_min
                width = x_max - x_min
                height = y_max - y_min

                # 다각형 면적 구하기, 사선 공식 이용
                plus = 0
                minus = 0
                for idx in range(len(points[0])-1):
                    # 현재의 x좌표점을 다음 y좌표점과 곱해줘서 더해줌
                    plus += points[0][idx] * \
                        points[1][(idx+1) % len(points[1])]
                    # 현재의 y좌표점을 다음 x좌표점과 곱해줘서 더해줌
                    minus += points[1][idx] * \
                        points[0][(idx+1) % len(points[0])]
                area = math.fabs(0.5 * (plus - minus))
                anno_no += 1
                AnnotationsData.append({"segmentation": [annotation['points']], "image_id": image_no, "category_id": int(
                    annotation['class_id']), "area": area, "bbox": [x_center, y_center, width, height], "id": anno_no, "iscrowd": 0})

        self.dataset["images"] = ImagesData
        self.dataset["annotations"] = AnnotationsData
        self.dataset["categories"] = [
            {
                "supercategory": "Water",
                "id": 1,
                "name": "Water"
            },
            {
                "supercategory": "Vehicle",
                "id": 2,
                "name": "Vehicle"
            },
            {
                "supercategory": "Road",
                "id": 3,
                "name": "Road"
            },
            {
                "supercategory": "Farmland",
                "id": 4,
                "name": "Farmland"
            },
            {
                "supercategory": "Greenhouse",
                "id": 5,
                "name": "Greenhouse"
            },
            {
                "supercategory": "Temporary building",
                "id": 6,
                "name": "Temporary building"
            },
            {
                "supercategory": "Bale silage",
                "id": 7,
                "name": "Bale silage"
            },
            {
                "supercategory": "Tent",
                "id": 8,
                "name": "Tent"
            },
            {
                "supercategory": "Trash",
                "id": 9,
                "name": "Trash"
            }]

    def get_Dataset(self, output_dir, file_name):
        output_path = os.path.join(output_dir, file_name+".json")
        with open(output_path, "w") as json_file:
            json.dump(self.dataset, json_file)
        return output_path


if __name__ == '__main__':
    ano_test_dir = r"C:\Users\ohanthony\Desktop\Data\asan_resize\annfiles\test"
    ano_train_dir = r"C:\Users\ohanthony\Desktop\Data\asan_resize\annfiles\train"
    ano_val_dir = r"C:\Users\ohanthony\Desktop\Data\asan_resize\annfiles\val"
    img_test_dir = r"C:\Users\ohanthony\Desktop\Data\asan_resize\images\test"
    img_train_dir = r"C:\Users\ohanthony\Desktop\Data\asan_resize\images\train"
    img_val_dir = r"C:\Users\ohanthony\Desktop\Data\asan_resize\images\val"
    test = To_CocoDataset(img_test_dir, ano_test_dir).get_Dataset(
        ano_test_dir, "test")
    train = To_CocoDataset(img_train_dir, ano_train_dir).get_Dataset(
        ano_train_dir, "train")
    val = To_CocoDataset(img_val_dir, ano_val_dir).get_Dataset(
        ano_val_dir, "val")

    print("success!")
