import cv2

# Initialize the camera (use bigger indices if you use multiple cameras)
cap = cv2.VideoCapture(0)
# Set the video resolution to half of the possible max resolution for better performance
cap.set(3, 1920 / 2)
cap.set(4, 1080 / 2)

while True:
    # Read frame from camera stream and convert it to greyscale
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Show image in cv2 window
    cv2.imshow("image", img)
    # Break if input key equals "ESC"
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
