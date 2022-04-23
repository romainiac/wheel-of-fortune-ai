import cv2
#import numpy as np
import functools

cap = cv2.VideoCapture('assets/video2.mp4')

class Tile:
    def __init__(self, x, y, w, h, color):
        self.x = x;
        self.y = y;
        self.w = w;
        self.h = h;
        self.color = color;

# sort by coordinates
# y coorindate comes first, if y is the same within an allowence, x comes first
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

# check to see if tile a is within tile b
def isWithin(a, b):
    a_top_left = (a.x, a.y)
    a_top_right = (a.x + a.w, a.y)
    b_bottom_left = (a.x, a.y + a.h)
    c_bottom_right = (a.x + w, a.y + h)

    b_top_left = (a.x, a.y)
    b_top_right = (a.x + a.w, a.y)
    b_bottom_left = (a.x, a.y + a.h)
    b_bottom_right = (a.x + w, a.y + h)

    return False

while cap.isOpened():
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # threshhold sweetspot for white tiles
    mask_white = cv2.inRange(img, (0,0,205), (255,50,255))
    contours_white, hierarchy = cv2.findContours(mask_white,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    with_contours = frame
    #with_contours = cv2.drawContours(frame, contours_white, -1,(255,0,255),3)

    # threshhold sweetspot for the green tiles
    mask_green = cv2.inRange(img, (67,47,67), (98,255,255))
    contours_green, hierarchy = cv2.findContours(mask_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #with_contours = cv2.drawContours(frame, contours_green, -1,(0,255,255),3)


    tiles = []
    # Draw a bounding box around all contours for white
    for c in contours_white:
        x, y, w, h = cv2.boundingRect(c)
         # Make sure contour area is large enough
        if (cv2.contourArea(c)) > 1500:
            x,y,w,h = cv2.boundingRect(c)
            if (h > w and h / 2 < w and w * h < 5000):
                tiles.append(Tile(x,y,w,h,"white"))
                #cv2.rectangle(with_contours,(x,y), (x+w,y+h), (251,72,196), 2)

    # Draw a bounding box around all contours
    for c in contours_green:
        x, y, w, h = cv2.boundingRect(c)
        # Make sure contour area is large enough
        if (cv2.contourArea(c)) > 1500:
            x,y,w,h = cv2.boundingRect(c)
            if (h > w and h / 2 < w and w * h < 5000):
                tiles.append(Tile(x,y,w,h,"green"))
                #cv2.putText(with_contours, "(" + str(x) + "," + str(y) + ")", (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0), 1, cv2.LINE_AA)
                #cv2.rectangle(with_contours,(x,y), (x+w,y+h), (0,255,255), 2)
    
    # sort tiles
    tiles = sorted(tiles, key=functools.cmp_to_key(sort))

    # go through tiles and remove the ones that are located within the bound of another box
    # this will handle the cases where letters are treated as boxes
    # since they are sorted, the ones the remove (if any) will be next to each other) so we can avoid n^2
    # we might also only want to check it if its a white tile 
    for i in range(len(tiles)):
        cur_tile = tiles[i];
        to_remove = []

        # check left
        if (i - 1 >= 0):
            left_tile = tiles[i - 1];
            if isWithin(left_tile, cur_tile) and left_tile.color == 'white' and cur_tile.color == 'white': 
                to_remove.append(left_tile)
        #check right
        if (i + 1 < len(tiles)):
            right_tile = tiles[i + 1];
            if isWithin(right_tile, cur_tile) and right_tile.color == 'white' and cur_tile.color == 'white': 
                to_remove.append(right_tile)

        for tile in to_remove: tiles.remove(tile)


    for i in range(len(tiles)):
        tile = tiles[i]
        box_color = (251,72,196) #pink 
        if tile.color == 'green': 
            box_color = (0,255,255) # yellow

        cv2.rectangle(with_contours, (tile.x, tile.y), (tile.x + tile.w, tile.y + tile.h), box_color, 2)
        cv2.putText(with_contours, str(i), (tile.x, tile.y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

    words = ""
    for tile in tiles:
        if tile.color == "white":
            words += "_ "
        else:
            words += ' '

    words = words.strip()
    print(words)
    cv2.imshow('All contours with bounding box', with_contours)

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

