from glob import glob
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import *
import sys
import os

os.makedirs("gradients", exist_ok=True)

exts = "mp4 webm".split()


if len(sys.argv) < 2:
	print("directory path missing")

#paths = [sys.argv[1]]

path = sys.argv[1]

paths = []
for ext in exts:
	paths += glob(f"{path}/*.{ext}")

print(len(paths), "found")

for path in paths:
	#if os.path.getsize(path) >= 5e6:
	#	continue

	clip = VideoFileClip(path)

	w = 1
	h = 480

	colors = []

	n = 0
	for frame in clip.iter_frames():
		#print(n)
		img = Image.fromarray(frame)
		img = img.resize((w,h)).convert("RGB")
		imgarr = np.array(img, dtype=np.float)
		color = np.mean(imgarr, axis=(0,1))
		color = np.array(np.round(color), dtype=np.uint8)
		colors.append(tuple(color))
		n += 1

	print(path, ":", n, "frames")

	out = Image.new("RGB", (n*w,h))
	draw = ImageDraw.Draw(out)
	for c, color in enumerate(colors):
		draw.line((c,0,c,h), color)
	
	out.save(f"gradients/{os.path.basename(path)}.png")
	#out.show()
