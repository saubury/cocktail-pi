import sys
import getopt
import os.path
import picamera
import time
import boto3
import json
import os
import hashlib
import re
import datetime
import config


def quickAudioMsg(audiotext, presound='eventually.mp3', voice='Emma'):
    file_mp3 = './cache/' + cache_filename(audiotext) + '.mp3'

    if (os.path.exists(file_mp3)):
        playMP3('./sounds/{}'.format(presound), background=True)
        time.sleep(0.8)
    else:
        playMP3('./sounds/{}'.format(presound), background=True)
        client = boto3.client('polly')
        response = client.synthesize_speech(OutputFormat='mp3', Text=audiotext, VoiceId=voice)    
        thebytes = response['AudioStream'].read()
        thefile = open(file_mp3, 'wb')
        thefile.write(thebytes)
        thefile.close()

    playMP3(file_mp3, background=False)

def playMP3(file_mp3, background):
    if background:
        os.system('mpg123 -q ' + file_mp3 + ' 2>/dev/null &')
    else:
        os.system('mpg123 -q ' + file_mp3 + ' 2>/dev/null')

def takePhotoAndProcess():
    namebase='./tmp/snapped_{}'.format(datetime.datetime.today().strftime('%Y%m%d-%H%M%S'))
    file_jpg=namebase + '.jpg'
    file_json=namebase + '.json'
    emotion = 'unknown'
    age_range_low = 10
    if (not os.path.exists(file_jpg) or not os.path.exists(file_json)):
        with picamera.PiCamera() as camera:
            camera.capture(file_jpg)

        with open(file_jpg, 'rb') as f_file_jpg:
            b_a_jpg = bytearray(f_file_jpg.read())
            rclient = boto3.client('rekognition')
            response = rclient.detect_faces(Image={    'Bytes': b_a_jpg}, Attributes=['ALL'])
        with open(file_json, 'w') as outfile:
            json.dump(response, outfile)

        gender, emotion, age_range_low = processJSON(file_json)
    return gender, emotion, age_range_low


def processJSON(file_json):
    with open(file_json) as data_file:    
        data = json.load(data_file)

    age_range_low=data["FaceDetails"][0]["AgeRange"]["Low"]
    age_range_high=data["FaceDetails"][0]["AgeRange"]["High"]
    gender=data["FaceDetails"][0]["Gender"]["Value"]

	# Sort; and find the highest confidence emotion
    json_obj = data["FaceDetails"][0]
    sorted_obj = sorted(json_obj['Emotions'], key=lambda x : x['Confidence'], reverse=True)
    emotion = sorted_obj[0]['Type']

    return gender, emotion, age_range_low

def cache_filename(filename):
    # make a legal filename, remove spaces and punctuation - and limit to 50 characters
    hashstring = hashlib.md5(filename).hexdigest()
    fileprefix = re.sub('[^a-zA-Z0-9]', '_', filename).lower()[0:50]
    return fileprefix + hashstring

if __name__ == '__main__':
    quickAudioMsg("Hello world!!!")
