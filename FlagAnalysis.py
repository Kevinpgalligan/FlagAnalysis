#!python3

# A program to analyse the flags of the world.
# Images taken from: http://flagpedia.net/download

from PIL import Image
import os
import time

    
def create_avg_flag (images):
    """
    Averages a list of images to form a new image, saves the result.
    Note: images must have the same dimensions.
    
    This is done by going through each pixel and averaging the value stored
    at that co-ordinate over all the images.
    
    WARNING: takes a long time (~350s) to run. 
    
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
            x = k % avg.size[0]
            y = k // avg.size[0]
            avg_pixels[x, y] = (
                                (avg_pixels[x, y][0]*(n+1) + img[k][0]) // (n+2),
                                (avg_pixels[x, y][1]*(n+1) + img[k][1]) // (n+2),
                                (avg_pixels[x, y][2]*(n+1) + img[k][2]) // (n+2)
                               )
                               
    avg.save('results/average_flag.jpg')


def main():
    names = [('flags/' + name) for name in os.listdir('flags')]
    images = [Image.open(name) for name in names]
    create_avg_flag2(images)

if __name__ == '__main__':
	main()