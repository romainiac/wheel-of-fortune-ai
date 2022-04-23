import cv2


img = cv2.imread('assets/3.png')
img = cv2.resize(img, (1920,1080))

#convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask_white = cv2.inRange(hsv, (0,0,205), (255,50,255))
contours_white, hierarchy = cv2.findContours(mask_white,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

mask_green = cv2.inRange(hsv, (67,47,67), (98,255,255))
contours_green, hierarchy = cv2.findContours(mask_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for c in contours_white:
    x, y, w, h = cv2.boundingRect(c)
    if (cv2.contourArea(c)) > 3000:
        x,y,w,h = cv2.boundingRect(c)
        if (h > w and h / 2 < w and w * h < 10000):
            cv2.rectangle(img,(x,y), (x+w,y+h), (251,72,196), 3)

for c in contours_green:
    x, y, w, h = cv2.boundingRect(c)
    if (cv2.contourArea(c)) > 3000:
        x,y,w,h = cv2.boundingRect(c)
        if (h > w and h / 2 < w and w * h < 10000):
            cv2.rectangle(img,(x,y), (x+w,y+h), (0,255,255), 3)

cv2.imshow('contours_white', img)
cv2.imwrite('results/contours_green_with_bounds_3_3.png',img)


key = cv2.waitKey(0)

if key == 27:
    cv2.destroyAllWindows()
