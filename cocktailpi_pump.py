# Project Imports
import cocktailpi_config
import cocktailpi_util
import cocktailpi_aws
import RPi.GPIO as GPIO
import datetime
import time
import threading
from recipe import *

def pump_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(cocktailpi_config.gpio_pump_a, GPIO.OUT)
    GPIO.setup(cocktailpi_config.gpio_pump_b, GPIO.OUT)
    GPIO.setup(cocktailpi_config.gpio_pump_c, GPIO.OUT)
    GPIO.setup(cocktailpi_config.gpio_pump_d, GPIO.OUT)
    GPIO.setwarnings(True)

def pump_thread_runner(gpio_pump_name, run_seconds):
    GPIO.output(gpio_pump_name, GPIO.HIGH)
    time.sleep(run_seconds)
    GPIO.output(gpio_pump_name, GPIO.LOW)

def pump_thread_start(gpio_pump_name, run_seconds):
    thread = threading.Thread(target=pump_thread_runner, args=(gpio_pump_name, run_seconds))
    thread.start()

# Return the number of seconds to run
def lookup_time(drink_name, pump_name):
    ML_per_second = 1.9 

    try:
        num_ML = drink_name[pump_map[pump_name]]
        return num_ML / ML_per_second
    except KeyError:
        return 0

def do_drink(this_drink):
    pump_setup()

    (duration_a, duration_b, duration_c, duration_d) = (lookup_time(this_drink, "PUMP_A"), lookup_time(this_drink, "PUMP_B"), lookup_time(this_drink, "PUMP_C"), lookup_time(this_drink, "PUMP_D"))
    wait_time = max(duration_a, duration_b, duration_c, duration_d )
    msg = "Please be patient; your {} will be ready in {} seconds.".format(this_drink['Name'], int(wait_time))
    cocktailpi_aws.quickAudioMsg(msg)

    pump_thread_start(cocktailpi_config.gpio_pump_a, duration_a)
    pump_thread_start(cocktailpi_config.gpio_pump_b, duration_b)
    pump_thread_start(cocktailpi_config.gpio_pump_c, duration_c)
    pump_thread_start(cocktailpi_config.gpio_pump_d, duration_d)

    time.sleep(wait_time)
    msg = "Your drink, {}, is ready. Please enjoy.".format(this_drink['Name'])
    cocktailpi_aws.quickAudioMsg(msg, 'triumphant.mp3')

if __name__ == "__main__":
    do_drink('TEST')