from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import time
import cv2
import sys
import imutils
import RPi.GPIO as GPIO
import time

# Project Imports
import cocktailpi_config
import cocktailpi_util
import cocktailpi_servo
import cocktailpi_video
import cocktailpi_aws
import cocktailpi_button


def main():
    parser = argparse.ArgumentParser(description='Face processing puppy.')


    parser.add_argument("-x", "--servo_x", type=int, help="servo x setting")
    parser.add_argument("-y", "--servo_y", type=int, help="servo y setting")
    parser.add_argument("--videofile", help="pre recorded video file")
    parser.add_argument("--aws", help="test AWS")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-b", "--button", help="wait for external button press", action="store_true")
    parser.add_argument("-db", "--debugbutton", help="print a debug message on PCB button press", action="store_true")
    parser.add_argument("--noservo", help="surpress the servo", action="store_true")
    parser.add_argument("--livevideo", help="live video", action="store_true")
    parser.add_argument("--servodemo", help="demonstrate the servo", action="store_true")
    parser.add_argument("--showvideoframe", help="Display a video frame via XWindows", action="store_true")
    parser.add_argument("--novideo", help="Surpress a video frame via XWindows", action="store_true")
    
    args = parser.parse_args()

    cocktailpi_config.verbosemode= args.verbose
    cocktailpi_config.showvideoframe= args.showvideoframe
    cocktailpi_config.novideo= args.novideo

    if args.noservo:
        cocktailpi_config.servousage = False
        cocktailpi_util.printmsg("Servo turned off")

    if (args.livevideo):
        cocktailpi_servo.servo_on()
        cocktailpi_video.process_livevideo()
        cocktailpi_servo.servo_off()

    elif (args.button):
        cocktailpi_button.do_button()

    elif (args.aws):
        cocktailpi_aws.mainAWS(args.aws)

    elif args.videofile:
        cocktailpi_config.servousage = False
        cocktailpi_video.process_video(args.videofile)
 
    elif (args.servo_x >0 and args.servo_y >0):
        cocktailpi_servo.servo_on()
        cocktailpi_servo.servo_xy(args.servo_x, args.servo_y)
        cocktailpi_servo.servo_off()
        
    elif args.servodemo:
        cocktailpi_util.printmsg("Servo Demo")
        cocktailpi_servo.servo_on()
        cocktailpi_servo.servo_demo()
        cocktailpi_servo.servo_off()

    elif (args.debugbutton):
        cocktailpi_button.do_button_debug()



if __name__ == "__main__":
    try:
        main()

    finally:
        cocktailpi_servo.servo_off()
        cocktailpi_util.printmsg ("Cleanup and exit")


