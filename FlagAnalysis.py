#!python3

# A program to analyse the flags of the world.
# Images taken from: http://flagpedia.net/download

from PIL import Image
from matplotlib import pyplot as plt
import os
import sys

def create_avg_flag (images):
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
            # of images, but if it ain't broke don't fix it.
            avg_pixels[x, y] = (
                                (avg_pixels[x, y][0]*(n+1) + img[k][0]) // (n+2),
                                (avg_pixels[x, y][1]*(n+1) + img[k][1]) // (n+2),
                                (avg_pixels[x, y][2]*(n+1) + img[k][2]) // (n+2)
                               )
                               
    avg.save('results/average_flag.jpg')
    
def normalise_rgb(rgb):
    """Puts values of rgb tuples in 0-1 range."""
    s = rgb[0] + rgb[1] + rgb[2]
    if s:
        r = rgb[0] / s
        g = rgb[1] / s
        b = rgb[2] / s
    else:
        r, g, b = 0, 0, 0
    return (r, g, b)

def plot (images):
    """Saves bar chart of pixel colour frequency, small values are cut off."""
    pixel_count = {}

    # Count pixels.
    for n, img in enumerate(images):
        print("#{0}".format(n+1))
        for px in img.convert('RGB').getdata():
            if pixel_count.get(px):
                pixel_count[px] += 1
            else:
                pixel_count[px] = 1
    
    pairs = sorted([pair for pair in pixel_count.items()],
                            key=lambda pair: pair[0][0])
    colours = [normalise_rgb(pair[0]) for pair in pairs if pair[1] > 2000]
    frequency = [pair[1] for pair in pairs if pair[1] > 2000]
    
    plt.bar(range(len(frequency)), frequency,
            color=colours, edgecolor=colours
            )
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
    
    # plt.pie(frequency, colors=colours)
    # plt.title('Pixel Colour Frequency')
    # plt.savefig('results/piechart.png')
    

def main():
    args = sys.argv[1:]
    if not args:
        print("usage: [--chart] [--avg]")
        sys.exit(1)
    
    names = [('flags/' + name) for name in os.listdir('flags')]
    images = [Image.open(name) for name in names]
    
    if '--chart' in args:
        plot(images)
    
    if '--avg' in args:
        create_avg_flag(images)
    

if __name__ == '__main__':
	main()