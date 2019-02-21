# Face Detection

# Downloading haarcascade feature set from github

from BingImages import BingImages


def __downloadCascade():
    print("Downloading haarcascade for face detection")
    url = "https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml"
    folder = "./cascade/"
    local_filename = folder + url.split('/')[-1]
    # Check if already exists on users disk
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Stream download dataset to lcoal disk
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def liveFaceDetection(self):

    # Initialize the cascade classifier for detecting faces
    face_cascade = cv2.CascadeClassifier(
        "./face_cascade/haarcascade_frontalface_default.xml")

    # Initialize the camera (use bigger indices if you use multiple cameras)
    cap = cv2.VideoCapture(0)
    # Set the video resolution to half of the possible max resolution for better performance
    cap.set(3, 1920 / 2)
    cap.set(4, 1080 / 2)

    # Standard text that is displayed above recognized face
    exceptional_frames = 100
    while True:
        print(exceptional_frames)
        # Read frame from camera stream and convert it to greyscale
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces using cascade face detection
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Loop through detected faces and set new face rectangle positions
        for (x, y, w, h) in faces:
            color = (0, 255, 0)
            startpoint = (x, y)
            endpoint = (x + w, y + h)
            exceptional_frames = 0
            # Draw face rectangle on image frame
            cv2.rectangle(img, startpoint, endpoint, color, 2)

        # Show image in cv2 window
        cv2.imshow("image", img)
        # Break if input key equals "ESC"
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        exceptional_frames += 1

# Downloads resource images with the specified terms


def __resourceDownloader(self, count=300):
    for person in self.__persons:
        print("--Downloading Resources for '{}'".format(person))
        folder = "./tmp/downloaded_images/" + person
        # Fetch links from Bing Images and download images
        BingImages.download(BingImages(
            person + " face", count=count, person="portrait").get(), folder)
        counter = 0
        # Rename the files accordingly
        for filename in os.listdir(folder):
            filepath = folder + "/" + filename
            _, file_extension = os.path.splitext(filepath)
            # Remove files that are of wrong type or too small
            # File not jpeg smaller than 128kb
            if file_extension.lower() not in [".jpg", ".jpeg"] or os.path.getsize(filepath) < 1024*128:
                os.remove(filepath)
                continue
            tries = 0
            # Rename all other files with fitting schema "img_X.jpg"
            while(tries < 1000000):
                try:
                    os.rename(filepath, folder + "/" +
                              "image_" + str(counter) + ".jpg")
                    break
                # Catch error that a file may exist already with a certain name
                except FileExistsError:
                    tries += 1
                    counter += 1
                    pass
            counter += 1


BingImages.download(BingImages("Male Face", count=30,
                               person="portrait").get(), "./Males")
