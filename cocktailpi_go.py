# Project Imports
import cocktailpi_config
import cocktailpi_util
import cocktailpi_aws
import cocktailpi_servo
import cocktailpi_video
import cocktailpi_pump
import RPi.GPIO as GPIO
import datetime
import time

def button_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cocktailpi_config.gpio_button_green, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(cocktailpi_config.gpio_button_yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(cocktailpi_config.gpio_button_pcb, GPIO.IN)


def button_black():
    return GPIO.input(cocktailpi_config.gpio_button_green) == False

def switch_is_on():
    return GPIO.input(cocktailpi_config.gpio_button_yellow) == False

def button_pcb():
    return GPIO.input(cocktailpi_config.gpio_button_pcb) == False

def do_stuff():
    msg = 'Let me look at your face'
    cocktailpi_aws.quickAudioMsg(msg, 'chimes-glassy.mp3')
    file_string='./tmp/snapped_{}'.format(datetime.datetime.today().strftime('%Y%m%d-%H%M%S'))
    cocktailpi_aws.mainAWS(file_string)

    if switch_is_on():
        cocktailpi_pump.do_drink()


button_setup()
while True:
    if button_black():
        print('Button Pressed Black')
        do_stuff()

    if button_pcb():
        print('Button PCB Green')

    time.sleep(0.1)