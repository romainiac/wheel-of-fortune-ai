import cv2
import numpy as np
import functools
cap = cv2.VideoCapture('wheel_images/video2.mp4')

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
    allowence = 20;
    if abs(a.y - b.y) <= allowence: # check y first
        if abs(a.x - b.x) <= allowence:
            return 0;
        elif (a.x < b.x):
            return -1;
        return 1;
    elif a.y < b.y:
        return -1;
    else:
        return 1;

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
                cv2.rectangle(with_contours,(x,y), (x+w,y+h), (255,0,0), 2)

    # Draw a bounding box around all contours
    for c in contours_green:
        x, y, w, h = cv2.boundingRect(c)
        # Make sure contour area is large enough
        if (cv2.contourArea(c)) > 1500:
            x,y,w,h = cv2.boundingRect(c)
            if (h > w and h / 2 < w and w * h < 5000):
                tiles.append(Tile(x,y,w,h,"green"))
                #cv2.putText(with_contours, "(" + str(x) + "," + str(y) + ")", (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0), 1, cv2.LINE_AA)
                cv2.rectangle(with_contours,(x,y), (x+w,y+h), (0,0,255), 2)
    
    # sort tiles
    tiles = sorted(tiles, key=functools.cmp_to_key(sort))

    for i in range(len(tiles)):
        tile = tiles[i]
        cv2.putText(with_contours, str(i), (tile.x, tile.y), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0), 1, cv2.LINE_AA)

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

