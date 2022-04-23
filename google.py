from google.cloud import vision
import io
import cv2

# img = cv2.imread('wheel_images/1.png')

# client = vision.ImageAnnotatorClient()
# with io.open('wheel_images/1.png', 'rb') as image_file:
#     content = image_file.read()

# image = vision.Image(content=content)

# response = client.text_detection(image=image)
# texts = response.text_annotations

# for text in texts:
#     print(text)

# for text in texts:
#    cv2.rectangle(img_color, (x,hImg-y), (w, hImg-h), (0,0,255), 1)

#    print('\n"{}"'.format(text.description))

#   vertices = (['({},{})'.format(vertex.x, vertex.y)
#               for vertex in text.bounding_poly.vertices])

