# Project Imports
import config
import cloud
import pump
import RPi.GPIO as GPIO
import time
from recipe import *
import os

def button_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.gpio_button_green, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(config.gpio_button_yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(config.gpio_button_pcb, GPIO.IN)


def button_black():
    return GPIO.input(config.gpio_button_green) == False

def switch_is_on():
    return GPIO.input(config.gpio_button_yellow) == False

def button_green():
    return GPIO.input(config.gpio_button_pcb) == False

def do_bartender():
    msg = 'Hello, my name is Bridget your lovely bar tender. Please stay still, I am going to take a quick photo.'
    cloud.quickAudioMsg(msg)

    try:
        gender, emotion, age_range_low = cloud.takePhotoAndProcess()
    except (IndexError):
        cloud.quickAudioMsg('I can not see anyone at the bar')
        return
    
    msg = 'It is nice to meet a human {}. I think you are at least {} years old. You appear to be {}! '.format(gender, age_range_low, emotion)
    cloud.quickAudioMsg(msg)

    # Valid Values: HAPPY | SAD | ANGRY | CONFUSED | DISGUSTED | SURPRISED | CALM | UNKNOWN | FEAR
    if age_range_low < 25:
        drink_group = 'child'
        this_drink = recipe_limesoda
    else:
        drink_group = 'adult'
        if (emotion in [ 'HAPPY', 'CONFUSED', 'SURPRISED' ]):
            this_drink = recipe_vodkasodacranburry
        elif (emotion in [ 'ANGRY', 'DISGUSTED', 'FEAR' ]):
            this_drink = recipe_vodkalimesoda            
        else:
            this_drink = recipe_vodkasoda

    msg = "As you appear to be {}, I think an appropriate {} drink would be a {}. ".format(emotion, drink_group, this_drink['Name'])
    cloud.quickAudioMsg(msg)

    if switch_is_on():
        msg = "Press the green button for a {}, or the black button to cancel ".format(this_drink['Name'])
        cloud.quickAudioMsg(msg)
        while True:
            time.sleep(0.1)
            if button_black():
                cloud.quickAudioMsg("OK, cancelled")
                time.sleep(1)
                break;

            elif button_green():
                pump.do_drink(this_drink)
                break;



if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    button_setup()
    while True:
        if button_black():
            do_bartender()

        if button_green():
            cloud.quickAudioMsg('Boozy boozy. Boozy boozy. Would you like a Boozy boozy?')

        time.sleep(0.1)