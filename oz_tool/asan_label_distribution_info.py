import json
import os
from collections import defaultdict


def read_json_files_in_directory(directory_path):
    all_data = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                all_data.append(data)
    return all_data


def analyze_class_distribution(datasets):
    class_counts = defaultdict(int)
    total_annotation = 0
    for data in datasets:
        for annotation in data['Annotation']:
            class_id = annotation['class_id']
            class_counts[class_id] += 1
            total_annotation += 1
    return class_counts, total_annotation


def calculate_percentage(count, total):
    return (count / total) * 100 if total > 0 else 0


def main():
    class_id_labels = {
        '001': '물',
        '002': '자동차',
        '003': '도로',
        '004': '경작지',
        '005': '비닐하우스',
        '006': '가건물',
        '007': '곤포 사일리지',
        '008': '천막',
        '009': '쓰레기'
    }

    dataset_paths = {
        'train': '/home/ohanthony/datasets/asan/annfiles/train',
        'val': '/home/ohanthony/datasets/asan/annfiles/val',
        'test': '/home/ohanthony/datasets/asan/annfiles/test'
    }

    overall_distribution = {}

    for dataset_type, directory_path in dataset_paths.items():
        datasets = read_json_files_in_directory(directory_path)
        class_distribution, total_annotations = analyze_class_distribution(
            datasets)
        sorted_distribution = dict(sorted(class_distribution.items()))
        overall_distribution[dataset_type] = (
            sorted_distribution, total_annotations)

    output_path = '/home/ohanthony/datasets/asan/annfiles/ann_info.txt'
    with open(output_path, 'w') as out_file:
        for dataset_type, (distribution, total) in overall_distribution.items():
            out_file.write(f'"{dataset_type} 이미지 label 분포"\n')
            for class_id, count in distribution.items():
                percentage = calculate_percentage(count, total)
                label = class_id_labels.get(class_id, '알 수 없음')
                out_file.write(
                    f"{class_id} ({label}): {count}개 [{percentage:.2f}%]\n")
            out_file.write("\n")


if __name__ == "__main__":
    main()
