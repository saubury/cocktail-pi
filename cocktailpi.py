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

def isEnglish():
    return switch_is_on()

def button_black():
    return GPIO.input(config.gpio_button_green) == False

def switch_is_on():
    return GPIO.input(config.gpio_button_yellow) == False

def button_green():
    return GPIO.input(config.gpio_button_pcb) == False

def doBilingualMsg(msg_en, msg_fr, presound='eventually.mp3'):
    if isEnglish():
        cloud.quickAudioMsg(msg_en, presound=presound)
    else:
        cloud.quickAudioMsg(msg_fr, presound=presound, voice='Lea')


def do_bartender():
    msg_en = 'Hello, my name is Bridget your lovely bar tender. Please stay still, I am going to take a quick photo.'
    msg_fr = 'Bonjour, Je m''appelle Bridget'
    doBilingualMsg(msg_en, msg_fr)

    try:
        gender, emotion, age_range_low = cloud.takePhotoAndProcess()
    except (IndexError):
        doBilingualMsg('I can not see anyone at the bar', 'STUFF I can not see anyone at the bar')
        return
    
    msg_en = 'It is nice to meet a human {}. I think you are at least {} years old. You appear to be {}! '.format(gender, age_range_low, emotion)
    msg_fr = 'STUFF It is nice to meet a human {}. I think you are at least {} years old. You appear to be {}! '.format(gender, age_range_low, emotion)
    doBilingualMsg(msg_en, msg_fr)

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

    msg_en = "As you appear to be {}, I think an appropriate {} drink would be a {}. ".format(emotion, drink_group, this_drink['Name'])
    msg_fr = "STUFF As you appear to be {}, I think an appropriate {} drink would be a {}. ".format(emotion, drink_group, this_drink['Name'])
    doBilingualMsg(msg_en, msg_fr)


    msg_en = "Press the green button for a {}, or the black button to cancel ".format(this_drink['Name'])
    msg_fr = "STUFF Press the green button for a {}, or the black button to cancel ".format(this_drink['Name'])
    doBilingualMsg(msg_en, msg_fr)
    while True:
        time.sleep(0.1)
        if button_black():
            doBilingualMsg("OK, cancelled", "STUFF OK, cancelled")
            time.sleep(1)
            break;

        elif button_green():
            wait_time = pump.do_drink(this_drink)
            msg_en = "Please be patient; your {} will be ready in {} seconds.".format(this_drink['Name'], wait_time)
            msg_fr = "STUFF Please be patient; your {} will be ready in {} seconds.".format(this_drink['Name'], wait_time)
            doBilingualMsg(msg_en, msg_fr)
            time.sleep(wait_time)
            msg_en = "Your drink, {}, is ready. Please enjoy.".format(this_drink['Name'])
            msg_fr = "STUFF Your drink, {}, is ready. Please enjoy.".format(this_drink['Name'])
            doBilingualMsg(msg_en, msg_fr, 'triumphant.mp3')
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
            doBilingualMsg('Boozy boozy. Boozy boozy. Would you like a Boozy boozy?', 'STUFF Boozy boozy. Boozy boozy. Would you like a Boozy boozy?')

        time.sleep(0.1)