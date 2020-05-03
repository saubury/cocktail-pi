import time
import pigpio
import cocktailpi_config
import cocktailpi_util

def servo_on():
    pi = pigpio.pi() # Connect to local Pi.


def servo_centre():
    cocktailpi_util.printmsg('Servo centred')
    cocktailpi_config.servo_x = cocktailpi_config.x_mid
    cocktailpi_config.servo_y = cocktailpi_config.y_mid    
    servo_update()

def servo_delta(delta_x, delta_y):
    cocktailpi_config.servo_x += delta_x
    cocktailpi_config.servo_y += delta_y
    
    if (cocktailpi_config.servo_x < cocktailpi_config.x_min):
        cocktailpi_config.servo_x = cocktailpi_config.x_min
        
    if (cocktailpi_config.servo_x > cocktailpi_config.x_max):
        cocktailpi_config.servo_x = cocktailpi_config.x_max

    if (cocktailpi_config.servo_y < cocktailpi_config.y_min):
        cocktailpi_config.servo_y = cocktailpi_config.y_min
        
    if (cocktailpi_config.servo_y > cocktailpi_config.y_max):
        cocktailpi_config.servo_y = cocktailpi_config.y_max

    servo_update()

def servo_update():
    servo_xy(cocktailpi_config.servo_x, cocktailpi_config.servo_y)

def servo_xy(x, y):
    if (not cocktailpi_config.servousage):
        cocktailpi_util.printmsg("Servo Ignored :  x:{} y:{}".format(x, y))
        return
        
    cocktailpi_util.printmsg("Servo x:{} y:{}".format(x, y))
    pi = pigpio.pi() # Connect to local Pi.
    pi.set_servo_pulsewidth(cocktailpi_config.gpio_x,  x)
    pi.set_servo_pulsewidth(cocktailpi_config.gpio_y,  y)


def servo_demo():
    servo_centre()
    time.sleep(0.5)

    servo_delta(+150, 0)
    time.sleep(0.5)
    servo_delta(+150, 0)
    time.sleep(0.5)
    servo_delta(+150, 0)
    time.sleep(0.5)

    servo_delta(0, -150)
    time.sleep(0.5)
    servo_delta(0, -150)
    time.sleep(0.5)
    servo_delta(0, -150)
    time.sleep(0.5)

    servo_delta(-150, 0)
    time.sleep(0.5)
    servo_delta(-150, 0)
    time.sleep(0.5)
    servo_delta(-150, 0)
    time.sleep(0.5)

    time.sleep(0.5)
    servo_centre()

def servo_off():
    # switch servo off
    time.sleep(0.8)
    pi = pigpio.pi() # Connect to local Pi.
    pi.set_servo_pulsewidth(cocktailpi_config.gpio_x,  0);
    pi.set_servo_pulsewidth(cocktailpi_config.gpio_y,  0);
    pi.stop()
