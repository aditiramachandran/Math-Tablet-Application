import os
import sys
import random
import time

import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior 

BASEPATH="/home/nao/behaviors/"

import animacyStrings as anim


class Gesture:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stiffness = 1.0

        self.frame = None
        self.speechDevice = None
        self.motion = None
        self.posture = None
        self.led = None
        self.right = anim.right
        self.wrong = anim.wrong
        self.trouble = anim.trouble
        self.hint = anim.hint
        self.confused = anim.confused
        self.connectNao()
    
    
    def connectNao(self):
        #FRAME MANAGER FOR CALLING BEHAVIORS
        try:
            self.frame  = ALProxy("ALFrameManager", self.host, self.port)
        except Exception, e:
            print "Error when creating frame manager device proxy:"+str(e)
            exit(1)
        #POSTURE MANAGER#
        try:
            self.posture = postureProxy = ALProxy("ALRobotPosture", self.host, self.port)
        except Exception, e:
            print "Error creating posture proxy"+str(e)
            exit(1)

        #MOTION DEVICE FOR MOVEMENTS
        try:
            self.motion = ALProxy("ALMotion", self.host, self.port)
        except Exception, e:
            print "Error when creating motion device proxy:"+str(e)
            exit(1)

        #MAKE NAO STIFF (OTHERWISE IT WON'T MOVE)
        self.motion.stiffnessInterpolation("Body",self.stiffness,1.0)

        #MOTION DEVICE FOR MOVEMENTS
        try:
            self.led = ALProxy("ALLeds", self.host, self.port)
        except Exception, e:
            print "Error when creating led proxy:"+str(e)
            exit(1)

        #CONNECT TO A SPEECH PROXY
        try:
            self.speechDevice = ALProxy("ALTextToSpeech", self.host, self.port)
        except Exception, e:
            print "Error when creating speech device proxy:"+str(e)
            exit(1)


    def genSpeech(self, sentence):
        try:
            self.speechDevice.post.say(sentence)
        except Exception, e:
            print "Error when saying a sentence: "+str(e)

     
    def send_command(self, doBehavior):
        gesture_path = BASEPATH + doBehavior
        gesture_id   = self.frame.newBehaviorFromFile(gesture_path, "")
        self.frame.playBehavior(gesture_id)
        self.frame.completeBehavior(gesture_id)


    def goodbye(self):
        self.genSpeech(anim.finish)
        time.sleep(5)
        self.posture.goToPosture("SitRelax", 1.0)


    def intro(self):
        self.posture.goToPosture("Stand", 1.0)
        self.led.fadeListRGB("FaceLeds",[0x00FFFFFF],[0.1])

        self.genSpeech("Hello! My name is Nao, your personal robot tutor.")     

        self.genSpeech("Let's work on some math problems together.")
        time.sleep(8)


    def assess(self, what):
        if(what is "correct"):
            randnr = random.randint(0,len(self.right)-1)
            self.genSpeech(self.right[randnr])
            time.sleep(3)
        elif(what is "wrong"):
            randnr = random.randint(0,len(self.wrong)-1)
            self.genSpeech(self.wrong[randnr])
            time.sleep(3)
        elif(what is "trouble"):
            randnr = random.randint(0,len(self.trouble)-1)
            self.genSpeech(self.trouble[randnr])
            time.sleep(3)
        elif(what is "hint"): 
            randnr = random.randint(0,len(self.hint)-1)
            self.genSpeech(self.hint[randnr])
            time.sleep(3)
        elif(what is "confused"):
            randnr = random.randint(0,len(self.confused)-1)
            self.genSpeech(self.confused[randnr])
            time.sleep(3)


    def ask(self, question):
        self.genSpeech(question)
        time.sleep(2)

   
    def releaseNao(self):
        try:
            self.posture.goToPosture("SitRelax", 1.0)
            self.motion.stiffnessInterpolation("Body",0.0,self.stiffness)
        except Exception, e:
            print "Error when sitting down nao and making nao unstiff: "+str(e)
