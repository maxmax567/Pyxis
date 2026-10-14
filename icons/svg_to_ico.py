import cairosvg
import io
from PIL import Image

png_bytes = cairosvg.svg2png(url="icon.svg", output_width=256, output_height=256)
img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")

sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save("icon.ico", sizes=sizes)