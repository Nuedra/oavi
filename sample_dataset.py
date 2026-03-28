from pathlib import Path
from urllib.request import urlopen
from io import BytesIO
import json
from PIL import Image

origin = "https://www.slavcorpora.ru"
sample_id = "b008ae91-32cf-4d7d-84e4-996144e4edb7"
save_dir = Path("sample_images")
save_dir.mkdir(parents=True, exist_ok=True)

with urlopen(f"{origin}/api/samples/{sample_id}") as response:
    sample = json.loads(response.read().decode("utf-8"))
image_paths = [f"{origin}/images/{p['filename']}" for p in sample["pages"]]

for i, image_url in enumerate(image_paths, start=1):
    with urlopen(image_url) as response:
        data = response.read()
    image = Image.open(BytesIO(data)).convert("RGB")
    image.save(save_dir / f"img_{i:04d}.bmp")
