import cv2
import numpy as np
from fer import FER
from PIL import ImageDraw, Image
import os
import threading

data = []


def getframes():
    global get_frame
    get_frame = True
    while get_frame:
        global data
        data = vc.read()


# training
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faceRecognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8, 123)


def get_images():

    images = []
    labels = []
    number_labels = []
    number_label = 0

    try:
        image_paths = [os.path.join("Training_Data", f)
                       for f in os.listdir("Training_Data")]
    except FileNotFoundError:
        print("WARNING: No Training_Data folder found")
        return [], [], []

    for image_path in image_paths:
        gray = Image.open(image_path).convert('L')
        image = np.array(gray, 'uint8')

        id = image_path.split("\\")[1].split(".")[0]
        faces = faceCascade.detectMultiScale(
            image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            print('No face found in %s' % image_path)
            continue
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(id)
            number_labels.append(number_label)
            number_label += 1
            cv2.imshow("Training", image[y: y + h, x: x + w])
            cv2.waitKey(1)
    return images, labels, number_labels


images, labels, number_labels = get_images()
cv2.destroyAllWindows()

if len(labels) != 0:
    faceRecognizer.train(images, np.array(number_labels))

# End of training

vc = cv2.VideoCapture(0)
detector = FER(mtcnn=True)

thread = threading.Thread(target=getframes, args=())
thread.start()

while vc.isOpened():
    if len(data) < 1:
        continue
    try:
        image = cv2.resize(data[1], (672, 380))
    except Exception:
        print("Error decoding")
        continue
    face_detection_image_gray = Image.fromarray(image).convert("L")
    face_detection_image = np.array(face_detection_image_gray, 'uint8')

    emotions = detector.detect_emotions(image)

    faces_text = "No face detected"

    if (len(emotions) != 0):
        faces_text = "Face not recognised"
        top_emotion = max(emotions[0].get("emotions"),
                          key=emotions[0].get("emotions").get)
        faces = faceCascade.detectMultiScale(
            face_detection_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            if len(labels) == 0:
                faces_text = "No Training_Data"
                break
            number_predicted, conf = faceRecognizer.predict(
                face_detection_image[y: y + h, x: x + w])
            if number_predicted != -1:
                faces_text = "Face most likely to be %s" % labels[number_predicted]
                print("%s: %s, confidencec: %s" % (
                    labels[number_predicted], top_emotion, emotions[0].get("emotions").get(top_emotion)))

    # creating output image
    if (len(emotions) != 0):

        face_location = emotions[0].get("box")
        face_location[2] = face_location[0] + face_location[2]
        face_location[3] = face_location[1] + face_location[3]

        keys = []
        for key in emotions[0].get("emotions"):
            keys.append("%s: %s" %
                        (key, emotions[0].get("emotions").get(str(key))))
        emotions_text = "Emotions recognised:\n%s\n%s\n%s\n%s\n%s\n%s\n%s" % (
            keys[0], keys[1], keys[2], keys[3], keys[4], keys[5], keys[6])
    else:
        face_location = [-1, -1, -1, -1]
        emotions_text = "No emotions recognisd"

    output_image = Image.fromarray(image)
    image_width, image_height = output_image.size
    draw = ImageDraw.Draw(output_image)
    draw.rectangle((face_location[0], face_location[1],
                   face_location[2], face_location[3]), outline="green", width=2)
    draw.text((10, 50), emotions_text, fill="green")
    draw.text((10, image_height - 20), faces_text, fill="green")
    final_output_image = np.array(output_image, 'uint8')
    cv2.imshow("Press ESC to close", final_output_image)

    key = cv2.waitKey(1)
    if (key == 27):
        get_frame = False
        thread.join()
        vc.release()
        cv2.destroyAllWindows()
