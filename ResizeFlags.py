#!python3

"""
Preliminary resizing of the images. Have to set them all to the same size
in order to make proper comparison.
"""

from PIL import Image
import os

# Collect images, store them with their names.
names = [('flags/' + name) for name in os.listdir('flags')]
images = [(name, Image.open(name)) for name in names]

# Have image/name pairs. Now to find the average width/height
# and set all images to match it.
avg_height = sum([img[1].size[0] for img in images]) // len(images)
avg_width = sum([img[1].size[1] for img in images]) // len(images)

new_image = None
for img in images:
    new_image = img[1].resize((avg_height, avg_width))
    new_image.save(img[0])