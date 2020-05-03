# Project Imports
import cocktailpi_config

def printmsg(mymsg):
    if (cocktailpi_config.verbosemode):
        print (">> {}".format(mymsg))
