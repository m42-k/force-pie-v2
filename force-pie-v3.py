#!/usr/bin/env python

## Base code written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
## This code is released into the public domain

## Overhauled for a different use BY m42-k!
## Raspberry Pi Model B+ 

## Import mrequired modules
import time
import os
import RPi.GPIO as GPIO
import sqlite3
from random import randint

global GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 

## Change to 1 to enable debug mode
DEBUG = 0

## Print a message and play a sound so the users knows its running
print "The Toy has been started!"
os.system('mpg123 -q /home/pi/kids-toy/kids-toy-box-2.mp3 &')

## read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
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
SPICLK = 18 ## (CLK) GPIO Pin 12
SPIMISO = 23 ## GPIO Pin 16
SPIMOSI = 24 ## GPIO Pin 18
SPICS = 25 ## (CS/SHDN) GPIO Pin 22

## LED GPIO numbers(BCM)
red_led = 21 ## Red - GPIO Pin 40
yellow_led = 20 # Yellow - GPIO Pin 38
green_led = 13 # Green - GPIO Pin 33

## Small FSR's connected to ADC
fsr_adc_red = 1 ## Red on Channel 1
fsr_adc_yellow = 2 ## Yellow on Channel 2
fsr_adc_green = 0 ## Green on Channel 0

## Set up LED GPIO pins
GPIO.setup(red_led, GPIO.OUT) ## Red
GPIO.setup(yellow_led, GPIO.OUT) ## Yellow
GPIO.setup(green_led, GPIO.OUT) ## Green

# Set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

## we'll assume that the blocks haven't been inserted yet
block_inserted_red = False ## Red
block_inserted_yellow = False ## Yellow
block_inserted_green = False ## Green

def play_audio():
        random_sound_file = randint(1,5)
        if random_sound_file == 1:
                os.system('mpg123 -q /home/pi/kids-toy/its-fun-to-count-2.mp3 &')
        if random_sound_file == 2:
                os.system('mpg123 -q /home/pi/kids-toy/one-two-three-2.mp3 &')
        if random_sound_file == 3:
                os.system('mpg123 -q /home/pi/kids-toy/one-two-three-four-five-2.mp3 &')
        if random_sound_file == 4:
                os.system('mpg123 -q /home/pi/kids-toy/one-two-three-its-fun-to-count-2.mp3 &')
        if random_sound_file == 5:
                os.system('mpg123 -q /home/pi/kids-toy/one-two-three-whole-thing-2.mp3 &')

# Functions that run on Force Detection
def red_block_in(): ## Red
        GPIO.output(red_led, True)
        
def yellow_block_in(): ## Yellow
        GPIO.output(yellow_led, True)
        
def green_block_in(): ## Green
        GPIO.output(green_led, True)
        
## Update Databse Functions
def database_counter(colour):
        try:
                connection = sqlite3.connect('../kids-toy/toy_box.db')
                toy_box_db = connection.cursor()
        except:
                print "Sorry, unable to connect to database"
                
        ## Database Query to update counter
        add_to_database_sql = "UPDATE blocks\
        SET block_count = block_count + 1\
        WHERE block_colour = '"+colour+"'"
        
        if DEBUG:
                print "\nEntire database contents:\n"
                for row in toy_box_db.execute("SELECT * FROM blocks"):
                        print row
        
        ## Execute Database Query
        toy_box_db.execute(add_to_database_sql)
        
        ## Commit database changes
        connection.commit()
        
        ## Close databse connection
        toy_box_db.close()
        connection.close()

## Keep track of the last FSR value
last_fsr_read_red = 0 ## Red 
last_fsr_read_yellow = 0 ## Yellow
last_fsr_read_green = 0 ## Green

## Add a tolerance for FSR sensitivity
red_tolerance = 100 ## Red
yellow_tolerance = 80 ## Yellow
green_tolerance = 80 ## Green
                    
while True:
        ## We'll assume that the blocks haven't been inserted yet
        block_inserted_red = False ## Red
        block_inserted_yellow = False ## Yellow
        block_inserted_green = False ## Green

        ## Read the signals from the FSR's
        fsr_signal_red = readadc(fsr_adc_red, SPICLK, SPIMOSI, SPIMISO, SPICS) ## Red
        fsr_signal_yellow = readadc(fsr_adc_yellow, SPICLK, SPIMOSI, SPIMISO, SPICS) ## Yellow
        fsr_signal_green = readadc(fsr_adc_green, SPICLK, SPIMOSI, SPIMISO, SPICS) ## Green
        
        ## How much has the FSR reading changed since the last read?
        fsr_adjust_red = fsr_signal_red - last_fsr_read_red ## Red
        fsr_adjust_yellow = fsr_signal_yellow - last_fsr_read_yellow ## Yellow
        fsr_adjust_green = fsr_signal_green - last_fsr_read_green ## Green
        
        if DEBUG:
                ## Red
                print "fsr_signal_red:", fsr_signal_red
                print "fsr_adjust_red:", fsr_adjust_red
                print "last_fsr_read_red:", last_fsr_read_red
                ## Yellow
                print "fsr_signal_yellow:", fsr_signal_yellow
                print "fsr_adjust_yellow:", fsr_adjust_yellow
                print "last_fsr_read_yellow:", last_fsr_read_yellow
                ## Green
                print "fsr_signal_green:", fsr_signal_green
                print "fsr_adjust_green:", fsr_adjust_green
                print "last_fsr_read_green:", last_fsr_read_green
                
        ## Conditions that determine if the block has been inserted
        ## Red
        if fsr_adjust_red > red_tolerance:
                block_inserted_red = True
        ## Yellow
        if fsr_adjust_yellow > yellow_tolerance:
                block_inserted_yellow = True
        ## Green
        if fsr_adjust_green > green_tolerance: 
                block_inserted_green = True
               
        if DEBUG:
                print "block_inserted_red:", block_inserted_red ## Red
                print "block_inserted_yellow:", block_inserted_yellow ## Yellow
                print "block_inserted_green:", block_inserted_green ## Green
        
        ## RED
        if block_inserted_red is True:
                red_block_in() ## Turn on Red LED
                database_counter("Red") # Add 1 to Red database counter
                play_audio() # Play random sound file
                
                ## Save the FSR reading for the next loop
                last_fsr_read_red = fsr_signal_red
        else:
                last_fsr_read_red = fsr_signal_red
                
        ## YELLOW
        if block_inserted_yellow is True:
                yellow_block_in() # Turn on Yellow LED
                database_counter("Yellow") # Add 1 to Yellow database counter
                play_audio() # Play random sound file
                
                ## Save the FSR reading for the next loop
                last_fsr_read_yellow = fsr_signal_yellow
        else:
                last_fsr_read_yellow = fsr_signal_yellow
                
        ## GREEN
        if block_inserted_green is True:
                green_block_in() ## Turn on Green LED
                database_counter("Green") # Add 1 to Green database counter
                play_audio() # Play random sound file
                
                ## Save the FSR reading for the next loop
                last_fsr_read_green = fsr_signal_green
        else:
                last_fsr_read_green = fsr_signal_green

        ## Hang out and do nothing for a half second
        time.sleep(0.3) 
        
        ## Turn LED's Off
        GPIO.output(red_led, False)
        GPIO.output(yellow_led, False)
        GPIO.output(green_led, False)
