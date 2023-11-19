from PIL import Image
import json
import os
import shutil


def resize_image(image_path, output_path, size):
    with Image.open(image_path) as img:
        img = img.resize(size)
        img.save(output_path)


def scale_points(points, original_size, target_size):
    scale_x = target_size[0] / original_size[0]
    scale_y = target_size[1] / original_size[1]

    scaled_points = []
    for i in range(0, len(points), 2):
        x = points[i] * scale_x
        y = points[i + 1] * scale_y
        scaled_points.extend([x, y])

    return scaled_points


def process_image_and_json(source_dir, output_dir, target_size):
    # Loop through train/val/test directories
    for split_dir in ['train', 'val', 'test']:
        input_image_dir = os.path.join(source_dir, 'images', split_dir)
        input_ann_dir = os.path.join(source_dir, 'annfiles', split_dir)
        output_image_dir = os.path.join(output_dir, 'images', split_dir)
        output_ann_dir = os.path.join(output_dir, 'annfiles', split_dir)

        # Create the output directories if they don't exist
        os.makedirs(output_image_dir, exist_ok=True)
        os.makedirs(output_ann_dir, exist_ok=True)

        for root, _, files in os.walk(input_image_dir):
            for file in files:
                if file.endswith(".tif"):
                    image_path = os.path.join(input_image_dir, file)
                    json_path = os.path.join(
                        input_ann_dir, os.path.splitext(file)[0] + ".json")

                    if os.path.exists(json_path):
                        # Load JSON data with utf-8 encoding
                        with open(json_path, 'r', encoding='utf-8') as json_file:
                            data = json.load(json_file)
                            if "Annotation" in data and data["Annotation"]:
                                original_size = (
                                    data["Images"]["image_width"], data["Images"]["image_height"])

                                # Resize the image
                                output_image_path = os.path.join(
                                    output_image_dir, file)
                                resize_image(
                                    image_path, output_image_path, target_size)

                                # Scale the points & points Update <== current: All Points update -- prev: Only one Points update
                                for idx, AnnotationVal in enumerate(data["Annotation"]):
                                    origin_points = AnnotationVal["points"]
                                    scaled_points = scale_points(
                                        origin_points, original_size, target_size)
                                    data["Annotation"][idx]["points"] = scaled_points

                                # Update the JSON data
                                data["Images"]["image_width"] = target_size[0]
                                data["Images"]["image_height"] = target_size[1]

                                # Save the updated JSON data to annfiles directory
                                output_json_path = os.path.join(
                                    output_ann_dir, os.path.splitext(file)[0] + ".json")
                                with open(output_json_path, 'w', encoding='utf-8') as json_file:
                                    json.dump(data, json_file,
                                              ensure_ascii=False, indent=4)
                            else:
                                # No Annotation found, just resize the image and copy JSON
                                output_image_path = os.path.join(
                                    output_image_dir, file)
                                resize_image(
                                    image_path, output_image_path, target_size)
                                shutil.copy(json_path, os.path.join(
                                    output_ann_dir, os.path.splitext(file)[0] + ".json"))


# 사용 예시
source_dir = 'D:\\1. Development\\project\\asan_split'
output_dir = 'C:\\Users\\ohanthony\\Desktop\\Data\\asan_resize'
target_size = (793, 793)
process_image_and_json(source_dir, output_dir, target_size)
