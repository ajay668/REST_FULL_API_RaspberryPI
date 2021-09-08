#Libraries
import flask
from flask import *

app = flask.Flask(__name__,template_folder = 'templates')
app.config["DEBUG"] =True


import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


# Displaying the the data on the website
@app.route('/', methods=['GET'])
def index():
    dist=distance()
    dist=round(dist,2)
    char_dist = str(dist)
    return render_template('index.html',char_dist=char_dist)


# Returning the data for GET request
@app.route('/sensor/data/jason', methods = ['GET'])
def app_json():
    dist=distance()
    dist=round(dist,2)
    char_dist = str(dist)
    
    dist_jason={'distance': char_dist}
    return jsonify(dist_jason)	


# NGROK is used to provide the url and provide a tunnel to the local host,
#default port address in the NGROK is 80 

if __name__ == '__main__':
    app.run(host='192.168.1.5', port=80)
 
