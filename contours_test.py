import cv2
import numpy as np

#Read input image
img = cv2.imread('wheel_images/1.png')

#convert from BGR to HSV color space
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#apply threshold
thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]

# find contours and get one with area about 180*35
# draw all contours in green and accepted ones in red
contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
#area_thresh = 0
min_area = 0.95*180*35
max_area = 1.05*180*35
result = img.copy()

result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
sensitivity = 50
lower = np.array([0,0,255-sensitivity])
upper = np.array([255,sensitivity,255])
result = cv2.inRange(result, lower, upper)

for c in contours:
    area = cv2.contourArea(c)
    cv2.drawContours(result, [c], -1, (0, 255, 0), 1)
    if area > min_area and area < max_area:
            cv2.drawContours(result, [c], -1, (0, 0, 255), 1)

# save result
cv2.imwrite("box_found.png", result)

cv2.imshow("RESULT", result)
cv2.waitKey(0)