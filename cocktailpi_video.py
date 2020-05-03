from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import imutils
import datetime


import cocktailpi_config
import cocktailpi_util
import cocktailpi_servo
import cocktailpi_button

capture_setup_x=320
capture_setup_y=240
ignore_threshold=3
delta_factor=0.8

def process_video(file_video):
    cocktailpi_util.printmsg('Video source:"{}"'.format(file_video))

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cocktailpi_config.file_cascPath)

    # capture frames from the camera
    cap = cv2.VideoCapture(file_video)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if frame is None:
            break
        process_frame(faceCascade, frame, False)


def process_livevideo():
    cocktailpi_util.printmsg('Live Video source')
    cocktailpi_button.button_setup()


    cocktailpi_servo.servo_centre()
    AwayFromCentre = False
    
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cocktailpi_config.file_cascPath)

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (capture_setup_x, capture_setup_y)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(capture_setup_x, capture_setup_y))

    # allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    FaceLastSeen = time.time()
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if cocktailpi_button.button_is_yellow():
            cocktailpi_util.printmsg("Button presset to stop tracking")
            cocktailpi_servo.servo_centre()
            cv2.destroyAllWindows()
            camera.close() 
            return 


        image = frame.array
        wasFaceFound = process_frame(faceCascade, image, True)
        rawCapture.truncate(0)
        if (wasFaceFound):
            FaceLastSeen = time.time()
            AwayFromCentre = True
        elif (AwayFromCentre and (time.time() - FaceLastSeen) > 5): # more than 5 seconds, recentre camera
            cocktailpi_util.printmsg("It's been a while - recente")
            cocktailpi_servo.servo_centre()
            AwayFromCentre = False
        
    

def process_frame(faceCascade, frame, alwaysShowFrame):
    retFaceFound = False
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.circle(frame, (x+w/2, y+h/2), int((w+h)/3), (0, 0, 255), 4)

    facesfound = len(faces)
    if facesfound > 0:
        retFaceFound = True
        cocktailpi_util.printmsg("Found {} faces. x:{}, y{}, z{}".format(len(faces), x+w/2, y+h/2, (w+h)/3))
        jpg_file='./tmp/face_found_{}.jpg'.format(datetime.datetime.today().strftime('%Y%m%d-%H%M%S'))
        cv2.imwrite(jpg_file, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        delta_x=(x+w/2-(capture_setup_x/2)) * - delta_factor
        delta_y=(y+h/2-(capture_setup_y/2)) *   delta_factor
        cocktailpi_util.printmsg('Delta x:{} y:{}'.format(delta_x,delta_y))
        if (delta_x>ignore_threshold or delta_x<-1*ignore_threshold or delta_y>ignore_threshold or delta_y<-1*ignore_threshold):
            cocktailpi_servo.servo_delta(delta_x,delta_y)

    if (not cocktailpi_config.novideo) and (alwaysShowFrame or facesfound > 0):
        cv2.imshow('frame',frame)
        key = cv2.waitKey(1) & 0xFF # wait until rendered

    return retFaceFound
