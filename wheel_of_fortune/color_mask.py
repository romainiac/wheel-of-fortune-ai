import cv2


img = cv2.imread('assets/3.png')

#convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask_white = cv2.inRange(hsv, (0,0,205), (255,50,255))

cv2.imshow('white_mask', mask_white)
#cv2.imwrite('results/mask_white.png',mask_white)
key = cv2.waitKey(0)

if key == 27:
    cv2.destroyAllWindows()
