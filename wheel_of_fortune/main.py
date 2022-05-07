# Title: Wheel of Fortune AI ?
# Author: Roman Yefimets
# Purpose: Given a video of a Wheel of Fortune phrase guessing event,
#          use image recognition to try to guess what the phrase is
#

import cv2
import functools
from cv2 import boundingRect
from cv2 import norm
from matplotlib.pyplot import contour
import numpy as np
import json
import pickle
cap = cv2.VideoCapture('assets/video2.mp4')

#a_temp = cv2.imread('letters/A.png')
#a_shape = cv2.inRange(a_temp, (0,0,0), (100,100,100))
#a_contours, heirarchy = cv2.findContours(a_shape,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

letter_temps = []

def normalize_contour(img):
    img = cv2.resize(img, (40,60))
    img = cv2.inRange(img, (0,0,0), (100,100,100))
    im, cnt = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(im) > 0:
        bounding_rect = cv2.boundingRect(im[0])
        img_cropped_bounding_rect = img[bounding_rect[1]:bounding_rect[1] + bounding_rect[3],
                                    bounding_rect[0]:bounding_rect[0] + bounding_rect[2]]

        #new_height = int((1.0 * img.shape[0])/img.shape[1] * 40.0)
        img_resized = cv2.resize(img_cropped_bounding_rect, (40, 60))
        return img_resized
    return None


def read_in_letter():
    a = cv2.imread("letters/A.png")
    a = normalize_contour(a)
    contours_a, h_a = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    letter_temps.append({"letter": "A", "contours": contours_a})

    r = cv2.imread("letters/R.png")
    r = normalize_contour(r)
    contours_r, h_a = cv2.findContours(r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    letter_temps.append({"letter": "R", "contours": contours_r})

    m = cv2.imread("letters/M.png")
    m = normalize_contour(m)
    contours_m, h_a = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    letter_temps.append({"letter": "M", "contours": contours_m})

    l = cv2.imread("letters/L.png")
    l = normalize_contour(l)
    contours_l, h_a = cv2.findContours(l, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    letter_temps.append({"letter": "L", "contours": contours_l})

    h = cv2.imread("letters/H.png")
    h = normalize_contour(h)
    contours_h, h_a = cv2.findContours(h, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    letter_temps.append({"letter": "H", "contours": contours_h})

    i = cv2.imread("letters/I.png")
    i = normalize_contour(i)
    contours_i, h_a = cv2.findContours(i, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    letter_temps.append({"letter": "I", "contours": contours_i})

    t = cv2.imread("letters/T.png")
    t = normalize_contour(t)
    contours_t, h_a = cv2.findContours(t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    letter_temps.append({"letter": "T", "contours": contours_t})

read_in_letter()

def find_closest_match(tile_contour):
    match = 100;
    tile_match = None
    for letter_contour in letter_temps:
        if len(tile_contour) > 0:
            cur_match = cv2.matchShapes(letter_contour["contours"][0], tile_contour[0], 1, 0.0)
            if cur_match < match:
                match = cur_match
                tile_match = letter_contour

    return tile_match

# Represents a Wheel of Fortune Tile
# containing the location of the tile on the screen and the type (white or green)
class Tile:
    def __init__(self, x, y, w, h, color):
        self.x = x;
        self.y = y;
        self.w = w;
        self.h = h;
        self.letter = ""
        self.color = color;

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # returns true if other tile is within this tile
    # returns false otherwise
    def contains(self, other):
        return self.x <= other.x and \
            self.y <= other.y and \
            self.x + self.w >= other.x + other.w and \
            self.y + self.h >= other.y + other.h and \
            self.x + self.w > other.x and \
            self.y + self.h > other.y


# Given two Tiles (a, b), sort them by coordinates
# top rows come first, left columns come first
# we will use an allowance since coordinates will not match
# exactly accross the same rows and columns
def sort(a, b):
    allowance = 20;
    if abs(a.y - b.y) <= allowance: # check y first
        if abs(a.x - b.x) <= allowance:
            return 0;
        elif (a.x < b.x):
            return -1;
        return 1;
    elif a.y < b.y:
        return -1;
    else:
        return 1;

# Main loop for reading in frames of a video
while cap.isOpened():
    ret, frame = cap.read()
    img_w, img_h = 1920, 1080
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    img = cv2.resize(frame, (img_w, img_h))
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    tiles = []
    min_tile_area = 1500
    max_tile_area = 5000

    # Find all the white tiles and add them to tiles list
    white_lower, white_upper = (0,0,205), (255,50,255)
    mask_white = cv2.inRange(img, white_lower, white_upper)
    contours_white, hierarchy = cv2.findContours(mask_white,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours_white:
        x,y,w,h = cv2.boundingRect(c)
        if cv2.contourArea(c) > min_tile_area:
            if h > w and h / 2 < w and w * h < max_tile_area:
                tiles.append(Tile(x,y,w,h,"white"))

    # Find all the green tiles and add them to tiles list
    mask_green = cv2.inRange(img, (67,47,67), (98,255,255))
    contours_green, hierarchy = cv2.findContours(mask_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours_green:
        x, y, w, h = cv2.boundingRect(c)
        if cv2.contourArea(c) > min_tile_area:
            if h > w and h / 2 < w and w * h < max_tile_area:
                tiles.append(Tile(x,y,w,h,"green"))

    
    # sort tiles
    tiles = sorted(tiles, key=functools.cmp_to_key(sort))

    # go through tiles and remove the ones that are located within the bound of another box
    # this will handle the cases where letters are treated as boxes
    # since they are sorted, the ones the remove (if any) will be next to each other) so we can avoid n^2
    # we might also only want to check it if its a white tile 
    to_remove = []
    for i in range(len(tiles)):
        cur_tile = tiles[i];

        # check left
        if (i - 1 >= 0):
            left_tile = tiles[i - 1];
            if cur_tile.contains(left_tile) and left_tile.color == 'white' and cur_tile.color == 'white': 
                 to_remove.append(left_tile)
        #check right
        if (i + 1 < len(tiles)):
            right_tile = tiles[i + 1];
            if cur_tile.contains(right_tile) and right_tile.color == 'white' and cur_tile.color == 'white': 
                to_remove.append(right_tile)

    for tile in to_remove: 
        if tile in tiles:
            tiles.remove(tile)

    # add an overlay to the main image to focus on the tiles
    overlay = frame.copy()
    cv2.rectangle(overlay, (0,0), (img_w, img_h), (0,0,0), -1)
    alpha = 0.9
    frame_with_overlay = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    #cv2.drawContours(frame_with_overlay, letter_temps[0]["contours"], 0, (0,255,0), 2)

    # Draw a box around white and green tiles
    for i in range(len(tiles)):
        tile = tiles[i]
        box_color = (251,72,196) #pink 
        if tile.color == 'green': 
            box_color = (0,255,255) # yellow
        if tile.color == 'white':
            letter_img = frame[tile.y: tile.y + tile.h, tile.x: tile.x + tile.w]
            letter_img_resize = normalize_contour(letter_img)
            letter_contours_white, heirarchy = cv2.findContours(letter_img_resize, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            match = find_closest_match(letter_contours_white)
            if match != None:
                #cv2.drawContours(letter_img, match["contours"][0], -1, (0,255,255), 2)
                cv2.drawContours(letter_img, letter_contours_white[0], -1, (0,0,255), 2)
                cv2.putText(frame_with_overlay, match["letter"], (tile.x, tile.y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            #if total_match < .009:
            #    cv2.putText(frame_with_overlay, "A", (tile.x, tile.y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            #    print(total_match)
            cv2.putText(frame_with_overlay, tile.letter, (tile.x, tile.y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            frame_with_overlay[tile.y: tile.y + tile.h, tile.x: tile.x + tile.w] = letter_img

        #cv2.rectangle(frame, (tile.x, tile.y), (tile.x + tile.w, tile.y + tile.h), box_color, 2)
        #cv2.putText(frame, str(i), (tile.x, tile.y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

    cv2.imshow('main', frame_with_overlay)

    words = ""
    for tile in tiles:
        if tile.color == "white":
            words += "_ "
        else:
            words += ' '

    words = words.strip()

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

