from glob import glob
import numpy as np
from PIL import Image
from moviepy.editor import *
import sys
import os

os.makedirs("averages", exist_ok=True)

exts = "mp4 webm".split()


if len(sys.argv) < 2:
	print("directory path missing")

path = sys.argv[1]

if "." in path:
	paths = [path]
else:
	paths = []
	for ext in exts:
		paths += glob(f"{path}/*.{ext}")

print(len(paths), "found")

for path in paths:
	#if os.path.getsize(path) >= 5e6:
	#	continue

	clip = VideoFileClip(path)

	w = 640
	h = 480

	arr = np.zeros((h,w,3), np.float)

	n = 0
	for frame in clip.iter_frames():
		#print(n)
		img = Image.fromarray(frame)
		img = img.resize((w,h)).convert("RGB")
		imgarr = np.array(img, dtype=np.float)
		arr = arr + imgarr
		n += 1

	arr /= n

	arr = np.array(np.round(arr), dtype=np.uint8)

	print(path, ":", n, "frames")

	out = Image.fromarray(arr, mode="RGB")
	out.save(f"averages/{os.path.basename(path)}.png")
	#out.show()
