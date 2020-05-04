# Project Imports
import cocktailpi_config
import cocktailpi_util
import RPi.GPIO as GPIO
import datetime
import time
import threading


pump_map = {"PUMP_A": "Gin", "PUMP_B": "Tonic", "PUMP_C": "Cordial", "PUMP_D": "Vermouth"}
recipe_gnt = {"Gin": 5, "Tonic": 20}
recipe_martini  = {"Gin": 12, "Vermouth": 18}
recipe_everything = {"Gin": 1, "Tonic": 2, "Vermouth": 3, "Cordial": 4}

this_drink = recipe_gnt


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

def lookup_time(drink_name, pump_name):
    try:
        return drink_name[pump_map[pump_name]]
    except KeyError:
        return 0

pump_setup()





pump_thread_start(cocktailpi_config.gpio_pump_a, lookup_time(this_drink, "PUMP_A"))
pump_thread_start(cocktailpi_config.gpio_pump_b, lookup_time(this_drink, "PUMP_B"))
pump_thread_start(cocktailpi_config.gpio_pump_c, lookup_time(this_drink, "PUMP_C"))
pump_thread_start(cocktailpi_config.gpio_pump_d, lookup_time(this_drink, "PUMP_D"))


