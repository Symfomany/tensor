import cv2

vidcap = cv2.VideoCapture()
vidcap.open(0)
retval, image = vidcap.retrieve()
vidcap.release()
cv2.imwrite("test.png", image)
