import os
import sys
import random
import time

import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior
import almath 

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
        self.wrong_postfix = anim.wrong_postfix
        self.trouble = anim.trouble
        self.hint = anim.hint
        self.confused = anim.confused
        self.connectNao()
    
    
    def connectNao(self):
        #FRAME MANAGER FOR CALLING BEHAVIORS
        try:
            print 'in connect nao, host and port are:', self.host, ',', self.port
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

    def move_head(self):
        #self.posture.goToPosture("Sit", 1.0)

        self.motion.setStiffnesses("Head", 1.0)
        # Example showing multiple trajectories
        # Interpolate the head yaw to 1.0 radian and back to zero in 2.0 seconds
        # while interpolating HeadPitch up and down over a longer period.
        #names  = ["HeadYaw","HeadPitch"]
        names = ["HeadPitch"]
        # Each joint can have lists of different lengths, but the number of
        # angles and the number of times must be the same for each joint.
        # Here, the second joint ("HeadPitch") has three angles, and
        # three corresponding times.
        #angleLists  = [[50.0*almath.TO_RAD, 0.0],
        #           [-30.0*almath.TO_RAD, 30.0*almath.TO_RAD, 0.0]]
        angleLists = [-10.0*almath.TO_RAD, 20.0*almath.TO_RAD, 0.0]
        #timeLists   = [[1.0, 2.0], [ 1.0, 2.0, 3.0]]
        timeLists = [ 1.0, 2.0, 3.0]
        isAbsolute  = True
        
        self.genSpeech("hello my name is nao")
        for j in range(5):
            self.motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)

            #time.sleep(1.0)
        #self.motion.setStiffnesses("Head", 0.0)
        

    def assess(self, what):
        if(what is "correct"):
            randnr = random.randint(0,len(self.right)-1)
            self.genSpeech(self.right[randnr])
            time.sleep(3)
        elif(what is "wrong"):
            randnr = random.randint(0,len(self.wrong_postfix)-1)
            self.genSpeech(self.wrong_postfix[randnr])
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
