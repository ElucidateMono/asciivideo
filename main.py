# -*- coding: cp1252 -*-
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import cv2
import os
import imageio
#import shutil
import time


def ascii_to_image(name, ascii, SIZE):
    SIZE = SIZE*10
    img = Image.new("RGB",(SIZE - int((SIZE/2.5)),SIZE),"white")
    draw = ImageDraw.Draw(img)
    draw.text((0,0), ascii, (0,0,0))
    img.resize((640,480))
    img.save("imgs/" + str(name) + ".jpg")
    
def image_to_ascii(image):
    ascii_char = ["@", "#", "£", "=", "+", "|", ":", "."] #This shit needs fixing af. Better ascii shades plz.
    SIZE = 200 # This will determine the total size of the file. So 200 = 200 x 200
    (image_w, image_h) = image.size
    ratio = int(image_h / float(image_w)) #We want an aspect ratio so the image looks finesse af and not as wonky as someone's dick.
    if ratio == 0:
        ratio = 1
    current_image = image.resize((SIZE, ratio * SIZE)) #We want the width to be scaled to smth like 200 x 200 while maintaining ratio so quick mafs.
    current_image = current_image.convert("L") #Convert to black and white(grayscale) to make our life easier.
    pixels = list(current_image.getdata()) # Get the pixel data as a list so we can loop through that shit.
    pixel_image_data = ""
    for pixel in pixels: # We've sorta split this shit up in a way that allows us to pull from the ASCII char table based on darkness. 0 is black, 255 white.
        pixel_image_data += ascii_char[int(pixel/36)] #If we divide it up by 36, then we have 50 shades of gr- I mean, 8 shades of ASCII.
    pixel_image = [] #Lonely list.
    for x in range(0, len(pixel_image_data), SIZE): #Spliting it up so every 200 chars we go to a new line, 200 x 200, got that ASPECT RaTIO
        pixel_image.append(pixel_image_data[x:x+SIZE]) #Add that to the list so we can combine it with new lines characters easily.
    return "\n".join(pixel_image) #Join it up with newlines so it prints nicely.

def video_to_images(name):
    if not os.path.exists("ascii"):
        os.mkdir("ascii")
    if not os.path.exists("caps"):
        os.mkdir("caps")
    if not os.path.exists("ascii"):
        os.mkdir("ascii")
    if not os.path.exists("imgs"):
        os.mkdir("imgs")
    print("Converting video to image frames...")
    t1 = time.time()
    cap = cv2.VideoCapture(name)
    success, image = cap.read()
    image = cv2.resize(image, (640,480))
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    while success:
        cv2.imwrite("caps/%d.jpg" % count, image)
        success,image = cap.read()
        image = cv2.resize(image, (640,480))
        count += 1
    print("Saved %d frames to caps folder." % count)
    print("Took %d seconds." % time.time() - t1)
    return fps
    
def video_images_to_ascii():
    imgs = os.listdir("caps")
    print("Converting %d frames to ascii." % len(imgs))
    t1 = time.time()
    count = 0
    for image in imgs:
        i = Image.open("caps/" + image)
        asc = image_to_ascii(i)
        with open("ascii/" + str(count) + ".txt", "w") as f:
            f.write(asc)
        count += 1
    print("Converted all frames to ascii.")
    print("Took %d seconds!" % time.time() - t1)
    #shutil.rmtree("caps")

def third_stage():
    t1 = time.time()
    print("Converting all ascii back to images.")
    items = os.listdir("ascii")
    count = 0
    for item in items:
        with open("ascii/" + item, "r") as f:
            asc = f.read()
        ascii_to_image(count, asc, 200)
        count += 1
        if (count % 1000) == 0:
            print("Currently done %s frames." % count)
    print("Done")
    print("Took %d seconds" % (time.time()-t1))
    #shutil.rmtree("ascii")

def final_stage_gif():
    print("Finally, collating it all into one big gif...")
    with imageio.get_writer("output.gif", mode="I") as writer:
        for img in os.listdir("imgs"):
            image = imageio.read("imgs/" + img)
            writer.append_data(image)
    print("Done!")
    #shutil.rmtree("imgs")


def final_stage(fps):
    t1 = time.time()
    print("Finally, converting it to an AVI video file...")
    os.system("ffmpeg -i imgs/%d.jpg -r " + str(fps) + " -vcodec mpeg4 -y output.mp4")
    print("Finished!")
    print("Took %d seconds!" % time.time() - t1)


fps = video_to_images("test.avi")
video_images_to_ascii()
third_stage()
final_stage(fps)
