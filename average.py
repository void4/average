from glob import glob
import numpy as np
from PIL import Image

exts = "png jpg jpeg".split()

paths = []

for ext in exts:
	#TODO: make case insensitive
	paths += glob(f"*.{ext}")

print(paths)

w = 640
h = 480

arr = np.zeros((h,w,3), np.float)

n = 0
for path in paths:
	img = Image.open(path)
	img = img.resize((w,h)).convert("RGB")
	imgarr = np.array(img, dtype=np.float)
	arr = arr + imgarr
	n += 1

arr /= n

arr = np.array(np.round(arr), dtype=np.uint8)

print(n, "images")

out = Image.fromarray(arr, mode="RGB")
out.save("average.png")
out.show()
