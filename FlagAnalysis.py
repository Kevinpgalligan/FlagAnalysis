#!python3

# A program to analyse the flags of the world.
# Images taken from: http://flagpedia.net/download

from PIL import Image
from matplotlib import pyplot as plt
import os
import sys
import math
import collections
import numpy as np
import progressbar as progressbar

# As per: https://htmlcolorcodes.com/
# Since it looks ugly if we count the frequency
# of every RGB combination, we instead "round"
# the colours to the nearest of these common
# colours.
COMMON_COLOURS = np.array([
    [255, 255, 255], # white
    [192, 192, 192], # silver
    [128, 128, 128], # gray
    [  0,   0,   0], # black
    [255,   0,   0], # red
    [128,   0,   0], # maroon
    [255, 255,   0], # yellow
    [128, 128,   0], # olive
    [  0, 255,   0], # lime
    [  0, 128,   0], # green
    [  0, 255, 255], # aqua
    [  0, 128, 128], # teal
    [  0,   0, 255], # blue
    [  0,   0, 128], # navy
    [255,   0, 255], # fuchsia
    [128,   0, 128]  # purple
])
COMMON_COLOURS_MAP = [tuple(colour) for colour in COMMON_COLOURS]
def euclidean_dist(rgb1, rgb2):
    return math.sqrt(sum((rgb1[i] - rgb2[i])**2 for i in range(3)))

def nearest_common_colour(rgb):
    return min(COMMON_COLOURS, key=lambda c: euclidean_dist(rgb, c))

def create_avg_flag(images):
    """
    Averages a list of images to form a new image, saves the result.
    Note: images must have the same dimensions.
    
    This is done by going through each pixel and averaging the value stored
    at that co-ordinate over all the images.
    
    WARNING: takes ~350s to run. 
    
    arguments:
        images  a list of images to be averaged.
    """
    
    avg = images[0].convert('RGB')
    avg_pixels = avg.load()
    pixel_data = [img.convert('RGB').getdata() for img in images[1:]]
    
    print("Starting with #1...")
    x = y = 0
    for n, img in enumerate(pixel_data):
        print("#{}".format(n+2))
        for k, px in enumerate(img):
            # Convert flat list co-ordinates into 2D xy co-ordinates.
            x = k % avg.size[0]
            y = k // avg.size[0]
            
            # Adjust average value of pixel. It would be less horribly
            # inefficient to iterate through co-ordinates instead
            # of images.
            avg_pixels[x, y] = (
                                (avg_pixels[x, y][0]*(n+1) + img[k][0]) // (n+2),
                                (avg_pixels[x, y][1]*(n+1) + img[k][1]) // (n+2),
                                (avg_pixels[x, y][2]*(n+1) + img[k][2]) // (n+2)
                               )
                               
    avg.save('results/average_flag.jpg')
    
def plot(images):
    """Saves bar chart of pixel colour frequency."""
    colour_count = collections.defaultdict(int)

    for img in progressbar.progressbar(images):
        pixels = np.array(img.convert('RGB').getdata())
        # Messy code that gives a matrix D of size MxN, where
        # Dij is the Euclidean distance between the ith pixel
        # in the image and the jth common colour.
        diffs = np.concatenate(
                [np.sqrt(np.sum(np.square(pixels - colour), axis=1))
                 for colour in COMMON_COLOURS]) \
            .reshape((len(COMMON_COLOURS), len(pixels))).T
        for i in np.argmin(diffs, axis=1):
            colour_count[COMMON_COLOURS_MAP[i]] += 1

    colours = [(rgb[0]/255, rgb[1]/255, rgb[2]/255) for rgb, _ in colour_count.items()]
    counts = [f for _, f in colour_count.items()]

    plt.bar(range(len(counts)), counts, color=colours, edgecolor=(0, 0, 0))
    plt.ylabel('Frequency')
    plt.xlabel('Colour')
    plt.title('Pixel Colour Frequency', y=1.02)
    ax = plt.subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    left='off', right='off')
    plt.savefig('results/barchart.png')
    
    plt.clf()

def main():
    args = sys.argv[1:]
    if not args:
        print("usage: [--chart] [--avg]")
        sys.exit(1)
    
    names = sorted([('flags/' + name) for name in os.listdir('flags')])
    images = [Image.open(name) for name in names]

    if '--chart' in args:
        plot(images)

    if '--avg' in args:
        create_avg_flag(images)

if __name__ == '__main__':
	main()
