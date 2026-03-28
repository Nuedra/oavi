from pathlib import Path
import shutil

import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
PROJECT_DIR = BASE_DIR.parent
DATASET_DIR = PROJECT_DIR / "sample_images"

# ЛР4: работаем с изображениями №4, №9, №10 (нумерация с 1).
SELECTED_IMAGE_NUMBERS = (4, 9, 10)

# Вариант 1: оператор Робертса, G = sqrt(Gx^2 + Gy^2).


def load_rgb_image(path):
    image = Image.open(path).convert("RGB")
    return np.array(image, dtype=np.uint8)


def save_grayscale_image(path, array):
    Image.fromarray(array.astype(np.uint8), mode="L").save(path)


def rgb_to_grayscale_bt601(rgb):
    r = rgb[:, :, 0].astype(np.float64)
    g = rgb[:, :, 1].astype(np.float64)
    b = rgb[:, :, 2].astype(np.float64)
    gray = 0.3 * r + 0.59 * g + 0.11 * b
    return np.clip(gray, 0, 255).round().astype(np.uint8)


def normalize_to_uint8(array):
    arr = array.astype(np.float64)
    min_val = float(arr.min())
    max_val = float(arr.max())
    if max_val - min_val < 1e-12:
        return np.zeros(arr.shape, dtype=np.uint8)
    normalized = (arr - min_val) * 255.0 / (max_val - min_val)
    return np.clip(np.rint(normalized), 0, 255).astype(np.uint8)


def roberts_variant1(gray):
    src = gray.astype(np.float64)
    padded = np.pad(src, ((0, 1), (0, 1)), mode="edge")

    center = padded[:-1, :-1]
    right = padded[:-1, 1:]
    down = padded[1:, :-1]
    down_right = padded[1:, 1:]

    # Вариант 1 Робертса: Gx = e - i, Gy = f - h.
    gx = center - down_right
    gy = right - down
    g = np.sqrt(gx * gx + gy * gy)
    return gx, gy, g


def experimental_threshold(g_norm):
    # Эмпирический порог: верхние 20% значений считаем контуром.
    threshold = int(np.percentile(g_norm, 80))
    threshold = max(0, min(255, threshold))
    return threshold


def binarize(gray, threshold):
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
    gx, gy, g = roberts_variant1(gray)

    gx_norm = normalize_to_uint8(gx)
    gy_norm = normalize_to_uint8(gy)
    g_norm = normalize_to_uint8(g)
    threshold = experimental_threshold(g_norm)
    g_binary = binarize(g_norm, threshold)

    stem = path.stem
    save_grayscale_image(IMAGES_DIR / f"{stem}_02_gray.bmp", gray)
    save_grayscale_image(IMAGES_DIR / f"{stem}_03_gx_norm.bmp", gx_norm)
    save_grayscale_image(IMAGES_DIR / f"{stem}_04_gy_norm.bmp", gy_norm)
    save_grayscale_image(IMAGES_DIR / f"{stem}_05_g_norm.bmp", g_norm)
    save_grayscale_image(IMAGES_DIR / f"{stem}_06_g_binary.bmp", g_binary)

    print(
        f"{path.name}: T={threshold}, saved -> "
        f"{stem}_02_gray.bmp, {stem}_03_gx_norm.bmp, {stem}_04_gy_norm.bmp, "
        f"{stem}_05_g_norm.bmp, {stem}_06_g_binary.bmp"
    )


def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    selected_images = get_images_by_numbers(DATASET_DIR, SELECTED_IMAGE_NUMBERS)

    for image_path in selected_images:
        process_image(image_path)


if __name__ == "__main__":
    main()
