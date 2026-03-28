from pathlib import Path

import numpy as np
from PIL import Image


INPUT_IMAGE_PATH = Path(__file__).parent / "images" / "lab1.png"
OUTPUT_DIR = Path(__file__).parent / "images"

# Параметры для передискретизации
M = 3
N = 2


def load_rgb_image(path):
    image = Image.open(path).convert("RGB")
    return np.array(image, dtype=np.uint8)


def save_rgb_image(path, array):
    """Сохранить RGB."""
    Image.fromarray(array.astype(np.uint8), mode="RGB").save(path)


def save_grayscale_image(path, array):
    """Сохранить grayscale."""
    Image.fromarray(array.astype(np.uint8), mode="L").save(path)


def rgb_to_hsi(rgb):
    """RGB -> HSI."""
    rgb_norm = rgb.astype(np.float64) / 255.0
    r = rgb_norm[:, :, 0]
    g = rgb_norm[:, :, 1]
    b = rgb_norm[:, :, 2]

    intensity = (r + g + b) / 3.0

    min_rgb = np.minimum(np.minimum(r, g), b)
    sum_rgb = r + g + b
    saturation = np.zeros_like(intensity)
    nonzero = sum_rgb > 1e-12
    saturation[nonzero] = 1.0 - (3.0 * min_rgb[nonzero] / sum_rgb[nonzero])

    numerator = 0.5 * ((r - g) + (r - b))
    denominator = np.sqrt((r - g) ** 2 + (r - b) * (g - b))
    denominator = np.where(denominator < 1e-12, 1e-12, denominator)
    theta = np.arccos(np.clip(numerator / denominator, -1.0, 1.0))

    hue = np.where(b <= g, theta, 2.0 * np.pi - theta)
    hue = hue / (2.0 * np.pi)

    return hue, saturation, intensity


def hsi_to_rgb(h, s, i):
    """HSI -> RGB."""
    h_rad = (h % 1.0) * 2.0 * np.pi
    r = np.zeros_like(i)
    g = np.zeros_like(i)
    b = np.zeros_like(i)

    # Сектор 1: 0 <= H < 2*pi/3
    mask1 = (h_rad >= 0.0) & (h_rad < 2.0 * np.pi / 3.0)
    h1 = h_rad[mask1]
    b[mask1] = i[mask1] * (1.0 - s[mask1])
    r[mask1] = i[mask1] * (
        1.0 + s[mask1] * np.cos(h1) / np.cos(np.pi / 3.0 - h1 + 1e-12)
    )
    g[mask1] = 3.0 * i[mask1] - (r[mask1] + b[mask1])

    # Сектор 2: 2*pi/3 <= H < 4*pi/3
    mask2 = (h_rad >= 2.0 * np.pi / 3.0) & (h_rad < 4.0 * np.pi / 3.0)
    h2 = h_rad[mask2] - 2.0 * np.pi / 3.0
    r[mask2] = i[mask2] * (1.0 - s[mask2])
    g[mask2] = i[mask2] * (
        1.0 + s[mask2] * np.cos(h2) / np.cos(np.pi / 3.0 - h2 + 1e-12)
    )
    b[mask2] = 3.0 * i[mask2] - (r[mask2] + g[mask2])

    # Сектор 3: 4*pi/3 <= H < 2*pi
    mask3 = ~ (mask1 | mask2)
    h3 = h_rad[mask3] - 4.0 * np.pi / 3.0
    g[mask3] = i[mask3] * (1.0 - s[mask3])
    b[mask3] = i[mask3] * (
        1.0 + s[mask3] * np.cos(h3) / np.cos(np.pi / 3.0 - h3 + 1e-12)
    )
    r[mask3] = 3.0 * i[mask3] - (g[mask3] + b[mask3])

    rgb = np.stack([r, g, b], axis=2)
    rgb = np.clip(rgb, 0.0, 1.0)
    return (rgb * 255.0).round().astype(np.uint8)


def resize_nearest_one_pass(image, m, n):
    src_h, src_w = image.shape[:2]
    dst_h = max(1, (src_h * m) // n)
    dst_w = max(1, (src_w * m) // n)

    y_idx = (np.arange(dst_h) * n) // m
    x_idx = (np.arange(dst_w) * n) // m
    y_idx = np.clip(y_idx, 0, src_h - 1)
    x_idx = np.clip(x_idx, 0, src_w - 1)
    return image[y_idx[:, None], x_idx[None, :]]


def stretch_by_m(image, m):
    return resize_nearest_one_pass(image, m=m, n=1)


def compress_by_n(image, n):
    return resize_nearest_one_pass(image, m=1, n=n)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rgb = load_rgb_image(INPUT_IMAGE_PATH)

    # 1.1 Компоненты RGB
    red = np.zeros_like(rgb)
    red[:, :, 0] = rgb[:, :, 0]
    green = np.zeros_like(rgb)
    green[:, :, 1] = rgb[:, :, 1]
    blue = np.zeros_like(rgb)
    blue[:, :, 2] = rgb[:, :, 2]

    save_rgb_image(OUTPUT_DIR / "01_rgb_red_component.png", red)
    save_rgb_image(OUTPUT_DIR / "02_rgb_green_component.png", green)
    save_rgb_image(OUTPUT_DIR / "03_rgb_blue_component.png", blue)

    # 1.2 Яркостная компонента HSI
    h, s, intensity = rgb_to_hsi(rgb)
    intensity_img = np.clip(intensity * 255.0, 0, 255).round().astype(np.uint8)
    save_grayscale_image(OUTPUT_DIR / "04_hsi_intensity_component.png", intensity_img)

    # 1.3 Инверсия яркостной компоненты исходного изображения (в HSI)
    inv_i = 1.0 - intensity
    inverted_intensity_rgb = hsi_to_rgb(h, s, inv_i)
    save_rgb_image(OUTPUT_DIR / "05_hsi_inverted_intensity_rgb.png", inverted_intensity_rgb)

    # 2.1 Растяжение (интерполяция) в M раз
    stretched = stretch_by_m(rgb, M)
    save_rgb_image(OUTPUT_DIR / f"06_resample_stretch_x{M}.png", stretched)

    # 2.2 Сжатие (децимация) в N раз
    compressed = compress_by_n(rgb, N)
    save_rgb_image(OUTPUT_DIR / f"07_resample_compress_div{N}.png", compressed)

    # 2.3 Передискретизация в два прохода: сначала растяжение на M, затем сжатие на N
    two_pass = compress_by_n(stretched, N)
    save_rgb_image(
        OUTPUT_DIR / f"08_resample_two_pass_k_{M}_over_{N}.png",
        two_pass,
    )

    # 2.4 Однопроходная рациональная передискретизация K=M/N
    one_pass = resize_nearest_one_pass(rgb, M, N)
    save_rgb_image(
        OUTPUT_DIR / f"09_resample_one_pass_k_{M}_over_{N}.png",
        one_pass,
    )

if __name__ == "__main__":
    main()
