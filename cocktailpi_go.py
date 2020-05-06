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
from recipe import *

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

def do_bartender():
    msg = 'Hello, my name is Bridget your lovely bar tender. Please stay still, I am going to take a quick photo.'
    cocktailpi_aws.quickAudioMsg(msg)
    file_string='./tmp/snapped_{}'.format(datetime.datetime.today().strftime('%Y%m%d-%H%M%S'))
    emotion, age_range_low = cocktailpi_aws.mainAWS(file_string)

    print("age_range_low:{}".format(age_range_low))

    # Valid Values: HAPPY | SAD | ANGRY | CONFUSED | DISGUSTED | SURPRISED | CALM | UNKNOWN | FEAR
    if age_range_low < 18:
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

    if (emotion == 'TEST'):
        this_drink = recipe_test

    msg = "As you appear to be {}, I think an appropriate {} drink would be a {}. ".format(emotion, drink_group, this_drink['Name'])
    cocktailpi_aws.quickAudioMsg(msg)

    if switch_is_on():
        msg = "Press the green button for a {}, or the black button to cancel ".format(this_drink['Name'])
        cocktailpi_aws.quickAudioMsg(msg)
        while True:
            time.sleep(0.1)
            if button_black():
                print('Button Pressed Black')
                cocktailpi_aws.quickAudioMsg("OK, cancelled")
                time.sleep(1)
                break;
            elif button_pcb():
                print('Button PCB Green')
                cocktailpi_pump.do_drink(this_drink)
                break;



if __name__ == "__main__":
    button_setup()
    while True:
        if button_black():
            print('Button Pressed Black')
            do_bartender()

        if button_pcb():
            cocktailpi_aws.quickAudioMsg('Boozy boozy. Boozy boozy. Would you like a Boozy boozy?')

        time.sleep(0.1)