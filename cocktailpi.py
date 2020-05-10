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
    GPIO.setup(config.gpio_button_red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(config.gpio_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(config.gpio_button_blk, GPIO.IN)

def isEnglish():
    return switch_is_on()

def button_red():
    return GPIO.input(config.gpio_button_red) == False

def switch_is_on():
    return GPIO.input(config.gpio_switch) == False

def button_blk():
    return GPIO.input(config.gpio_button_blk) == False

def doBilingualMsg(msg_en, msg_fr, presound='eventually.mp3'):
    if isEnglish():
        cloud.quickAudioMsg(msg_en, presound=presound)
    else:
        cloud.quickAudioMsg(msg_fr, presound=presound, voice='Lea')


def do_bartender():
    msg_en = 'Hello, my name is Bridget your lovely bar tender. Please stay still, I am going to take a quick photo.'
    msg_fr = 'Bonjour, Je m''appelle Brigitte. Ne bougez pas, je vais vous prendre en photo.  Le petit oiseau va sortir'
    doBilingualMsg(msg_en, msg_fr)

    try:
        gender, emotion, age_range_low = cloud.takePhotoAndProcess()
    except (IndexError):
        doBilingualMsg('I can not see anyone at the bar', 'je ne vois personne au comptoir')
        return
    
    msg_en = 'It is nice to meet a human {}. I think you are at least {} years old. You appear to be {}! '.format(gender, age_range_low, emotion)
    msg_fr = 'Je suis ravie de rencontrer une personne {}. je crois que vous avez au moins {} ans. vous devez avoir {} ans! '.format(gender, age_range_low, emotion)
    doBilingualMsg(msg_en, msg_fr)

    # Valid Values: HAPPY | SAD | ANGRY | CONFUSED | DISGUSTED | SURPRISED | CALM | UNKNOWN | FEAR
    if age_range_low <25:
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

    map_emotion = {"HAPPY":"heureux", "SAD":"triste", "ANGRY":"en colere", "CONFUSED":"confuse", "DISGUSTED":"deguse", "SURPRISED":"surpris", "CALM":"calme", "UNKNOWN":"inconnue", "FEAR":"peur"}
    emotion_fr = map_emotion[emotion]

    msg_en = "As you appear to be {}, I think an appropriate {} drink would be a {}. ".format(emotion, drink_group, this_drink['Name'])
    msg_fr = "Comme vous semblez etre {}, je pense qu'une boisson appropriee pour un {} serait un {}. ".format(emotion_fr, drink_group, this_drink['Name'])
    doBilingualMsg(msg_en, msg_fr)


    msg_en = "Press the black button for a {}, or the red button to cancel ".format(this_drink['Name'])
    msg_fr = "Appuyez sur le bouton noir pour un {}, ou appuyez sur le bouton rougue pour annuler ".format(this_drink['Name'])
    doBilingualMsg(msg_en, msg_fr)
    while True:
        time.sleep(0.1)
        if button_red():
            doBilingualMsg("OK, cancelled", "OK, annule")
            time.sleep(1)
            break;

        elif button_blk():
            wait_time = pump.do_drink(this_drink)
            msg_en = "Please be patient; your {} will be ready in {} seconds.".format(this_drink['Name'], wait_time)
            msg_fr = "Merci de patienter; votre {} sera pret dans {} secondes.".format(this_drink['Name'], wait_time)
            doBilingualMsg(msg_en, msg_fr)
            time.sleep(wait_time)
            msg_en = "Your drink, {}, is ready. Please enjoy.".format(this_drink['Name'])
            msg_fr = "votre commande, {}, est prete. Bonne degustation.".format(this_drink['Name'])
            doBilingualMsg(msg_en, msg_fr, 'triumphant.mp3')
            break;

if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    button_setup()
    while True:
        if button_red():
            do_bartender()

        if button_blk():
            doBilingualMsg('Boozy boozy. Boozy boozy. Would you like a Boozy boozy?', 'Allez viens boire un petit coup!')

        time.sleep(0.1)
    