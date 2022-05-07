import cv2
import json
import numpy
import pickle
import io
import numpy_serializer as ns

a_temp = cv2.imread('letters/H.png')
a_temp = cv2.resize(a_temp, (100, 150))
a_shape = cv2.inRange(a_temp, (0,0,0), (100,100,100))
a_contours, heirarchy = cv2.findContours(a_shape,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#se = {"letter": "A", "contours" : json.dumps(pickle.dumps(a_contours).decode('latin-1'))}
    


#de = pickle.loads(json.loads(se).encode('latin-1'))


numpy.save("H.npy", a_contours, allow_pickle=True)
#arr = numpy.load("A.npy", allow_pickle=True)




