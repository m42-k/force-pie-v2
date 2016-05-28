#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

# HEAVILY MODIFIED BY m42-k!
# Raspberry Pi Model B+ Used

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
        
## GPIO numbers (BCM) used when connecting the ADC to the Raspberry Pi
SPICLK = 18 ## GPIO Pin 12
SPIMISO = 23 ## GPIO Pin 16
SPIMOSI = 24 ## GPIO Pin 18
SPICS = 25 ## GPIO Pin 22

## Small FSR's connected to ADC
fsr_adc_red = 0; ## Red on Channel 0
fsr_adc_yellow = 2; ## Yellow on Channel 2
fsr_adc_green = 4; ## Green on Channel 4

# LED GPIO numbers(BCM)
red_led = 21 ## Red - GPIO Pin 40
yellow_led = 20 # Yellow - GPIO Pin 38
green_led = 13 # Green - GPIO Pin 33

# Set up LED GPIO pins
GPIO.setup(red_led, GPIO.OUT) ## Red
GPIO.setup(yellow_led, GPIO.OUT) ## Yellow
GPIO.setup(green_led, GPIO.OUT) ## Green

# Set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# Functions that run on Force Detection
def red_block_in():
        GPIO.output(red_led, trim_pot_changed)
        time.sleep(1)

def green_block_in():
        GPIO.output(green_led, trim_pot_changed_green)
        time.sleep(1)

def yellow_block_in():
        GPIO.output(yellow_led, trim_pot_changed_yellow)
        time.sleep(1)

## Keep track of the last FSR value
last_fsr_read_red = 0 ## Red
last_fsr_read_yellow = 0 ## Yellow
last_fsr_read_green = 0 ## Green

## Add a tolerance for sensitivity allowances
tolerance = 5       # to keep from being jittery we'll only do an action
                    # when the force detected is over this amount
                    
while True:
        ## we'll assume that the blocks haven't been inserted yet
        block_inserted_red = False ## Red
        block_inserted_yellow = False ## Yellow
        block_inserted_green = False ## Green

        ## Read the signals from the FSR's
        fsr_signal_red = readadc(fsr_adc_red, SPICLK, SPIMOSI, SPIMISO, SPICS) ## Red
        fsr_signal_yellow = readadc(fsr_adc_yellow, SPICLK, SPIMOSI, SPIMISO, SPICS) ## Yellow
        fsr_signal_green = readadc(fsr_adc_green, SPICLK, SPIMOSI, SPIMISO, SPICS) ## Green
        
        ## How much has it changed since the last read?
        fsr_adjust_red = abs(fsr_signal_red - last_fsr_read_red) ## Red
        fsr_adjust_yellow = abs(fsr_signal_yellow - last_fsr_read_yellow) ## Yellow
        fsr_adjust_green = abs(fsr_signal_green - last_fsr_read_green) ## Green
        
        if DEBUG:
                ## Red
                print "fsr_signal_red:", fsr_signal_red
                print "fsr_adjust_yellow:", fsr_adjust_yellow
                print "last_fsr_read_red", last_fsr_read_red
                ## Yellow
                print "fsr_signal_yellow:", fsr_signal_yellow
                print "fsr_adjust_yellow:", fsr_adjust_yellow
                print "last_fsr_read_yellow", last_fsr_read_yellow
                ## Green
                print "fsr_signal_green:", fsr_signal_green
                print "fsr_adjust_green:", fsr_adjust_green
                print "last_fsr_read_green", last_fsr_read_green
        ## Red
        if ( fsr_adjust_red > tolerance ):
               block_inserted_red = True
        ## Yellow
        if ( fsr_adjust_yellow > tolerance ):
               block_inserted_yellow = True
        ## Green
        if ( fsr_adjust_green > tolerance ): 
               block_inserted_green = True

        if DEBUG:
                print "block_inserted_red", block_inserted_red ## Red
                print "block_inserted_yellow", block_inserted_yellow ## Yellow
                print "block_inserted_green", block_inserted_green ## Green
        
        ## RED
        if ( block_inserted_red ):
                red_block_in()
                #set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
                #set_volume = round(set_volume)          # round out decimal value
                #set_volume = int(set_volume)            # cast volume as integer

                #print 'Volume = {volume}%' .format(volume = set_volume)
                #set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
                #os.system(set_vol_cmd)  # set volume
                
                #if DEBUG:
                        #print "set_volume", set_volume
                        #print "trim_pot_changed", set_volume

                # save the potentiometer reading for the next loop
                last_fsr_read_red = fsr_adjust_red
                
        ## YELLOW
        if ( block_inserted_yellow ):
                yellow_block_in() 
                #set_volume_yellow = trim_pot_yellow / 10.24           # convert 10bit adc0 (0$
                #set_volume_yellow = round(set_volume_yellow)          # round out decimal val$
                #set_volume_yellow = int(set_volume_yellow)            # cast volume as integer

                #print 'Volume = {volume_yellow}%' .format(volume_yellow = set_volume_yellow)
                #set_vol_cmd_yellow = 'sudo amixer cset numid=1 -- {volume_yellow}% > /dev/null' .format(volume_yellow = set_volume_yellow)
                #os.system(set_vol_cmd_yellow)  # set volume
                
                #if DEBUG:
                        #print "set_volume_yellow", set_volume_yellow
                        #print "trim_pot_changed_yellow", set_volume_yellow

                # save the potentiometer reading for the next loop 
                last_fsr_read_yellow = fsr_adjust_yellow
                
        ## GREEN
        if ( block_inserted_green ):
                green_block_in() 
                #set_volume_green = trim_pot_green / 10.24           # convert 10bit adc0 (0$
                #set_volume_green = round(set_volume_green)          # round out decimal val$
                #set_volume_green = int(set_volume_green)            # cast volume as integer

                #print 'Volume = {volume_green}%' .format(volume_green = set_volume_green)
                #set_vol_cmd_green = 'sudo amixer cset numid=1 -- {volume_green}% > /dev/null' .format(volume_green = set_volume_green)
                #os.system(set_vol_cmd_green)  # set volume
                
                #if DEBUG:
                        #print "set_volume_green", set_volume_green
                        #print "trim_pot_changed_green", set_volume_green

                # save the potentiometer reading for the next loop  
                last_fsr_read_green = fsr_adjust_green

        # hang out and do nothing for a half second
        time.sleep(0.5)
        GPIO.output(red_led, False)
        GPIO.output(yellow_led, False)
        GPIO.output(green_led, False)