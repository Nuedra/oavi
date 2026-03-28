from pathlib import Path
import shutil

import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
PROJECT_DIR = BASE_DIR.parent
DATASET_DIR = PROJECT_DIR / "sample_images"
SELECTED_IMAGE_NUMBERS = (1, 2, 3)


def load_grayscale_image(path):
    image = Image.open(path).convert("L")
    return np.array(image, dtype=np.uint8)


def save_grayscale_image(path, array):
    Image.fromarray(array.astype(np.uint8), mode="L").save(path)


def spatial_smoothing_3x3(gray):
    src = gray.astype(np.float64)
    padded = np.pad(src, pad_width=1, mode="edge")

    smoothed = (
        padded[:-2, :-2]
        + padded[:-2, 1:-1]
        + padded[:-2, 2:]
        + padded[1:-1, :-2]
        + padded[1:-1, 1:-1]
        + padded[1:-1, 2:]
        + padded[2:, :-2]
        + padded[2:, 1:-1]
        + padded[2:, 2:]
    ) / 9.0

    return np.clip(np.rint(smoothed), 0, 255).astype(np.uint8)


def absolute_difference(a, b):
    diff = np.abs(a.astype(np.int16) - b.astype(np.int16))
    return diff.astype(np.uint8)


def contrast_multiply(gray, factor):
    boosted = gray.astype(np.int16) * int(factor)
    return np.clip(boosted, 0, 255).astype(np.uint8)


def get_diff_contrast_factor(path):
    stem = path.stem.lower()
    if stem.startswith("img_0001") or stem.startswith("img_0002"):
        return 10
    if stem.startswith("img_0003"):
        return 5
    return 1


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
    gray = load_grayscale_image(path)
    filtered = spatial_smoothing_3x3(gray)
    diff = absolute_difference(filtered, gray)
    factor = get_diff_contrast_factor(path)
    if factor > 1:
        diff = contrast_multiply(diff, factor=factor)

    filtered_path = IMAGES_DIR / f"{path.stem}_filtered.bmp"
    diff_path = IMAGES_DIR / f"{path.stem}_diff.bmp"
    save_grayscale_image(filtered_path, filtered)
    save_grayscale_image(diff_path, diff)

    print(f"{path.name}: saved -> {filtered_path.name}, {diff_path.name}")


def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    source_images = get_images_by_numbers(DATASET_DIR, SELECTED_IMAGE_NUMBERS)
    for image_path in source_images:
        process_image(image_path)


if __name__ == "__main__":
    main()
