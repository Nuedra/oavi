# Лабораторная работа №4

## Выделение контуров на изображении

**Вариант:** 1  
**Оператор:** Робертса (2x2)  
**Изображения выборки:** №4, №9, №10

---

## Используемый метод

Для каждого изображения выполнялись шаги:

1. Исходное цветное изображение переводилось в полутоновое по формуле:

```text
Y = 0.3R + 0.59G + 0.11B
```

2. Вычислялись компоненты градиента оператора Робертса (вариант 1):

```text
Gx = e - i
Gy = f - h
G  = sqrt(Gx^2 + Gy^2)
```

3. Матрицы `Gx`, `Gy`, `G` нормализовались в диапазон `[0..255]`.
4. Матрица `G` бинаризовалась по эмпирически подобранному порогу `T`.

Использованные пороги:

- `img_0004`: `T = 13`
- `img_0009`: `T = 8`
- `img_0010`: `T = 15`

---

## Результаты

### Изображение №4 (`img_0004`)

**Исходное цветное:**

<img src="./images/img_0004.bmp" alt="img_0004 original" width="700">

**Полутоновое:**

<img src="./images/img_0004_02_gray.bmp" alt="img_0004 gray" width="700">

**Градиент `Gx` (нормированный):**

<img src="./images/img_0004_03_gx_norm.bmp" alt="img_0004 gx norm" width="700">

**Градиент `Gy` (нормированный):**

<img src="./images/img_0004_04_gy_norm.bmp" alt="img_0004 gy norm" width="700">

**Модуль градиента `G` (нормированный):**

<img src="./images/img_0004_05_g_norm.bmp" alt="img_0004 g norm" width="700">

**Бинаризованная матрица `G`:**

<img src="./images/img_0004_06_g_binary.bmp" alt="img_0004 g binary" width="700">

### Изображение №9 (`img_0009`)

**Исходное цветное:**

<img src="./images/img_0009.bmp" alt="img_0009 original" width="700">

**Полутоновое:**

<img src="./images/img_0009_02_gray.bmp" alt="img_0009 gray" width="700">

**Градиент `Gx` (нормированный):**

<img src="./images/img_0009_03_gx_norm.bmp" alt="img_0009 gx norm" width="700">

**Градиент `Gy` (нормированный):**

<img src="./images/img_0009_04_gy_norm.bmp" alt="img_0009 gy norm" width="700">

**Модуль градиента `G` (нормированный):**

<img src="./images/img_0009_05_g_norm.bmp" alt="img_0009 g norm" width="700">

**Бинаризованная матрица `G`:**

<img src="./images/img_0009_06_g_binary.bmp" alt="img_0009 g binary" width="700">

### Изображение №10 (`img_0010`)

**Исходное цветное:**

<img src="./images/img_0010.bmp" alt="img_0010 original" width="700">

**Полутоновое:**

<img src="./images/img_0010_02_gray.bmp" alt="img_0010 gray" width="700">

**Градиент `Gx` (нормированный):**

<img src="./images/img_0010_03_gx_norm.bmp" alt="img_0010 gx norm" width="700">

**Градиент `Gy` (нормированный):**

<img src="./images/img_0010_04_gy_norm.bmp" alt="img_0010 gy norm" width="700">

**Модуль градиента `G` (нормированный):**

<img src="./images/img_0010_05_g_norm.bmp" alt="img_0010 g norm" width="700">

**Бинаризованная матрица `G`:**

<img src="./images/img_0010_06_g_binary.bmp" alt="img_0010 g binary" width="700">
