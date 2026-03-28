from pathlib import Path
import shutil

import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
PROJECT_DIR = BASE_DIR.parent
DATASET_DIR = PROJECT_DIR / "sample_images"
SELECTED_IMAGE_NUMBERS = (1, 2, 3)


def load_rgb_image(path):
    image = Image.open(path).convert("RGB")
    return np.array(image, dtype=np.uint8)


def save_grayscale_image(path, array):
    Image.fromarray(array.astype(np.uint8), mode="L").save(path)


def save_binary_image(path, array):
    binary_uint8 = np.where(array > 0, 255, 0).astype(np.uint8)
    Image.fromarray(binary_uint8, mode="L").save(path)


def rgb_to_grayscale_bt601(rgb):
    r = rgb[:, :, 0].astype(np.float64)
    g = rgb[:, :, 1].astype(np.float64)
    b = rgb[:, :, 2].astype(np.float64)
    gray = 0.3 * r + 0.59 * g + 0.11 * b
    return np.clip(gray, 0, 255).round().astype(np.uint8)


def balanced_histogram_threshold(gray):
    hist = np.bincount(gray.ravel(), minlength=256).astype(np.int64)

    left = 0
    right = 255
    while left < 255 and hist[left] == 0:
        left += 1
    while right > 0 and hist[right] == 0:
        right -= 1

    if left >= right:
        return int(left)

    weight_left = int(hist[left])
    weight_right = int(hist[right])

    while left < right:
        if weight_left < weight_right:
            left += 1
            weight_left += int(hist[left])
        else:
            right -= 1
            weight_right += int(hist[right])

    return int((left + right) // 2)


def binarize_by_threshold(gray, threshold):
    return np.where(gray > threshold, 255, 0).astype(np.uint8)


def get_images_by_numbers(dataset_dir, numbers):
    dataset_dir = Path(dataset_dir)
    paths = []
    for image_number in numbers:
        matches = sorted(dataset_dir.glob(f"img_{image_number:04d}.*"))
        if matches:
            paths.append(matches[0])
        else:
            raise FileNotFoundError(f"Не найдено изображение №{image_number} в {dataset_dir}")
    return paths


def process_image(path):
    shutil.copy2(path, IMAGES_DIR / path.name)
    rgb = load_rgb_image(path)
    gray = rgb_to_grayscale_bt601(rgb)
    threshold = balanced_histogram_threshold(gray)
    binary = binarize_by_threshold(gray, threshold)

    gray_path = IMAGES_DIR / f"{path.stem}_gray.bmp"
    binary_path = IMAGES_DIR / f"{path.stem}_binary.bmp"
    save_grayscale_image(gray_path, gray)
    save_binary_image(binary_path, binary)

    print(f"{path.name}: threshold={threshold}, saved -> {gray_path.name}, {binary_path.name}")


def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    source_images = get_images_by_numbers(DATASET_DIR, SELECTED_IMAGE_NUMBERS)

    for image_path in source_images:
        process_image(image_path)


if __name__ == "__main__":
    main()
