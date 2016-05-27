#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin): 
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
        
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18 
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# LED GPIO NUMBERS(BCM)
red_led = 21 # GPIO PIN 40
green_led = 13 # GPIO PIN 33
yellow_led = 20 # GPIO PIN 38

# SETUP LED GPIO PINS
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(yellow_led, GPIO.OUT)

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# Functions that run on Force Detection
def red_block_in():
        GPIO.output(red_led, trim_pot_changed)

def green_block_in():
        GPIO.output(green_led, trim_pot_changed_green)

def yellow_block_in():
        GPIO.output(yellow_led, trim_pot_changed_yellow)
  
# 10k trim pot connected to adc #0(RED), #1(GREEN) & #2(YELLOW)
fsr_adc_red = 0;
fsr_adc_yellow = 2;
fsr_adc_green = 4;

## RED
last_read = 0       # this keeps track of the last potentiometer value
## YELLOW
last_read_yellow = 0
## GREEN
last_read_green = 0
# RED & GREEN
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'
# YELLOW
tolerance_yellow = 5
                    
while True:
        # we'll assume that the pot didn't move
        ## RED
        trim_pot_changed = False
        ## YELLOW
        trim_pot_changed_yellow = False
        ## GREEN
        trim_pot_changed_green = False

        # read the analog pin
        ## RED
        trim_pot = readadc(fsr_adc_red, SPICLK, SPIMOSI, SPIMISO, SPICS)
        ## YELLOW
        trim_pot_yellow = readadc(fsr_adc_yellow, SPICLK, SPIMOSI, SPIMISO, SPICS)
        ## GREEN
        trim_pot_green = readadc(fsr_adc_green, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # how much has it changed since the last read?
        ## RED
        pot_adjust = abs(trim_pot - last_read)
        ## YELLOW
        pot_adjust_yellow = abs(trim_pot_yellow - last_read_yellow)
        ## GREEN
        pot_adjust_green = abs(trim_pot_green - last_read_green)
        
        if DEBUG:
                ## RED
                print "trim_pot:", trim_pot
                print "pot_adjust:", pot_adjust
                print "last_read", last_read
                ## YELLOW
                print "trim_pot_yellow:", trim_pot_yellow
                print "pot_adjust_yellow:", pot_adjust_yellow
                print "last_read_yellow", last_read_yellow
                ## GREEN
                print "trim_pot_green:", trim_pot_green
                print "pot_adjust_green:", pot_adjust_green
                print "last_read_green", last_read_green
        ## RED
        if ( pot_adjust > tolerance ):
               trim_pot_changed = True
        ## YELLOW
        if ( pot_adjust_yellow > tolerance_yellow ):
               trim_pot_changed_yellow = True
        ## GREEN
        if ( pot_adjust_green > tolerance ): 
               trim_pot_changed_green = True

        if DEBUG:
                ## RED
                print "trim_pot_changed", trim_pot_changed
                ## YELLOW
                print "trim_pot_changed_yellow", trim_pot_changed_yellow
                ## GREEN
                print "trim_pot_changed_green", trim_pot_changed_green
        
        ## RED
        if ( trim_pot_changed ):
                red_block_in()
                set_volume = trim_pot / 10.24           # convert 10bit adc0 (0$
                set_volume = round(set_volume)          # round out decimal val$
                set_volume = int(set_volume)            # cast volume as integer

                print 'Volume = {volume}%' .format(volume = set_volume)
                set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
                os.system(set_vol_cmd)  # set volume
                
                if DEBUG:
                        print "set_volume", set_volume
                        print "trim_pot_changed", set_volume

                # save the potentiometer reading for the next loop
                last_read = trim_pot
                
        ## YELLOW
        if ( trim_pot_changed_yellow ):
                yellow_block_in() 
                set_volume_yellow = trim_pot_yellow / 10.24           # convert 10bit adc0 (0$
                set_volume_yellow = round(set_volume_yellow)          # round out decimal val$
                set_volume_yellow = int(set_volume_yellow)            # cast volume as integer

                print 'Volume = {volume_yellow}%' .format(volume_yellow = set_volume_yellow)
                set_vol_cmd_yellow = 'sudo amixer cset numid=1 -- {volume_yellow}% > /dev/null' .format(volume_yellow = set_volume_yellow)
                os.system(set_vol_cmd_yellow)  # set volume
                
                if DEBUG:
                        print "set_volume_yellow", set_volume_yellow
                        print "trim_pot_changed_yellow", set_volume_yellow

                # save the potentiometer reading for the next loop 
                last_read_yellow = trim_pot_yellow
                
        ## GREEN
        if ( trim_pot_changed_green ):
                green_block_in() 
                set_volume_green = trim_pot_green / 10.24           # convert 10bit adc0 (0$
                set_volume_green = round(set_volume_green)          # round out decimal val$
                set_volume_green = int(set_volume_green)            # cast volume as integer

                print 'Volume = {volume_green}%' .format(volume_green = set_volume_green)
                set_vol_cmd_green = 'sudo amixer cset numid=1 -- {volume_green}% > /dev/null' .format(volume_green = set_volume_green)
                os.system(set_vol_cmd_green)  # set volume
                
                if DEBUG:
                        print "set_volume_green", set_volume_green
                        print "trim_pot_changed_green", set_volume_green

                # save the potentiometer reading for the next loop  
                last_read_green = trim_pot_green

        # hang out and do nothing for a half second
        time.sleep(0.5)
        GPIO.output(red_led, False)
        GPIO.output(yellow_led, False)
        GPIO.output(green_led, False)
