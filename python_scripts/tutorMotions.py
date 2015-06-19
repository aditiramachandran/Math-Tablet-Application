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
        self.auto_hint = anim.auto_hint
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
            id = self.speechDevice.post.say(sentence)
            return id
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

    def session_intro(self,sessionNum):
        print sessionNum
        if sessionNum == 1:
            self.genSpeech("Hello! My name is Nao. I am your personal robot tutor!")
            self.genSpeech("For each session, I have put fractions problems on the tablet in front of you.")
            self.genSpeech("Let's work on some problems together!")
        elif sessionNum == 2:
            self.genSpeech("Welcome back! Let's get started on our next session.")
        elif sessionNum == 3:
            self.genSpeech("Nice to see you again! Let's try doing some more problems!")
        elif sessionNum == 4:
            self.genSpeech("Hello again! Today is our last session. Let's get started!")
        else:
            print "invalid sessionNum: no intro"

    def intro(self):
        self.posture.goToPosture("Sit", 1.0)
        self.led.fadeListRGB("FaceLeds",[0x00FFFFFF],[0.1])

        self.genSpeech("Hello! My name is Nao, your personal robot tutor.")     
        self.genSpeech("Let's work on some fractions problems together.")
        #self.genSpeech("I'm going to put some problems on your tablet!")
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

    def wave(self):
        #this bit of code makes the robot wave
        self.posture.goToPosture("Sit", 1.0)
        #self.motion.closeHand("RHand")
        #self.motion.closeHand("LHand")
        self.genSpeech("i am now sitting")
        time.sleep(3)
        self.genSpeech("let me try to wave to you")
        time.sleep(2)

        self.motion.setAngles("RShoulderPitch",-1.0, 0.25)
        self.motion.setAngles("RShoulderRoll", -1.2, 0.25)
        self.motion.setAngles("RElbowRoll", 1.0, 0.25)
        self.motion.setAngles("RWristYaw", 0, 0.25)
        self.motion.openHand("RHand")
        #self.motion.setAngles("RShoulderRoll", -1.2, 0.5)
        #self.motion.setAngles("RHand", Open, 1.0)
        #self.motion.setAngles("RElbowRoll",angleBotElbow,0.3)

        #wave the hand 3 times, by moving the elbow
        self.motion.setAngles("RElbowRoll", 1.5, 0.5)
        time.sleep(0.5)
        self.motion.setAngles("RElbowRoll", 0.5, 0.5)
        time.sleep(0.5)
        self.motion.setAngles("RElbowRoll", 1.5, 0.5)
        time.sleep(0.5)
        self.motion.setAngles("RElbowRoll", 0.5, 0.5)
        time.sleep(0.5)
        self.motion.setAngles("RElbowRoll", 1.5, 0.5)
        time.sleep(0.5)
        self.motion.setAngles("RElbowRoll", 0.5, 0.5)
        time.sleep(0.5)
        self.motion.setAngles("RElbowRoll", 1.0, 0.5)
        time.sleep(0.5)
        self.genSpeech("hello there!")

        #self.genSpeech("now i will put my hand back down")
        time.sleep(2)
        self.motion.closeHand("RHand")
        self.posture.goToPosture("Sit", 1.0)
        
    def juddNelson(self):
        #this bit of code makes the robot thrust its hand into the air
        #start in sitting position
        self.posture.goToPosture("Sit", 1.0)
        self.genSpeech("i am now sitting")
        time.sleep(0.5)
        self.genSpeech("now i will raise my fist in the air")
        time.sleep(3)
        #move to position
        self.motion.setAngles("RShoulderPitch", -1.0, 0.5)
        self.motion.setAngles("RShoulderRoll", -1.3, 0.5)
        self.motion.setAngles("RElbowRoll", 1.5, 0.5)
        self.motion.setAngles("RWristYaw", 0, 0.5)
        self.motion.closeHand("RHand")
        time.sleep(1.0)
        self.genSpeech("good job! that's correct!")
        self.motion.setAngles("RShoulderRoll", -1.0, 0.25)
        self.motion.setAngles("RElbowRoll", 1.0, 0.5)
        #self.genSpeech("yay you did it!")
        #time.sleep(2)
        #self.genSpeech("now i will put my hand back down")
        time.sleep(2.5)
        self.posture.goToPosture("Sit", 1.0)

    def nod(self):
        #this bit of code makes the robot nod its head
        self.posture.goToPosture("Sit", 1.0)
        self.motion.setStiffnesses("Head", 1.0)
        self.genSpeech("i am now sitting")
        time.sleep(0.5)
        self.genSpeech("now i will nod my head")
        time.sleep(3)

        #move head
        #self.motion.setAngles("HeadPitch", 0, 0.5)
        #time.sleep(0.5)
        self.motion.setAngles("HeadPitch", 0.15, 0.25)
        time.sleep(0.5)
        self.motion.setAngles("HeadPitch", 0, 0.25)
        time.sleep(0.5)
        self.motion.setAngles("HeadPitch", 0.15, 0.25)
        time.sleep(0.5)
        self.genSpeech("yes, that's correct. good job!")

        #move back to original position
        time.sleep(3)
        self.posture.goToPosture("Sit", 1.0)

    def shake(self):
        #this bit of code makes the robot shake its head
        self.posture.goToPosture("Sit", 1.0)
        self.motion.setStiffnesses("Head", 1.0)
        self.genSpeech("i am now sitting")
        time.sleep(0.5)
        self.genSpeech("now i will shake my head")
        time.sleep(3)

        #shake head
        self.motion.setAngles("HeadPitch", 0, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", -0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", 0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", -0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", 0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", 0, 0.3)
        self.genSpeech("i'm sorry, that's incorrect. try again!")

        #move back to the original position
        time.sleep(0.5)
        self.posture.goToPosture("Sit", 1.0)

    def scale_up(self):
        #start position of the arm
        self.motion.setAngles("RShoulderPitch", 0.4, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RElbowYaw", 1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 0.4, 0.2)
        self.motion.setAngles("RWristYaw", 1.6, 0.2)
        self.motion.openHand("RHand")

        time.sleep(1)

        #end position of the arm
        self.motion.setAngles("RShoulderPitch", 0.4, 0.1)
        self.motion.setAngles("RElbowRoll", 1.3, 0.1)

        time.sleep(4)

        self.posture.goToPosture("Sit", 0.5)


    def scale_down(self):
        #start position of the arm
        self.motion.setAngles("RShoulderPitch", 0.7, 0.25)
        self.motion.setAngles("RShoulderRoll", -1.2, 0.25)
        self.motion.setAngles("RElbowYaw", 2.0, 0.3)
        self.motion.setAngles("RElbowRoll", 1.4, 0.25)
        self.motion.setAngles("RWristYaw", 0, 0.2)
        self.motion.openHand("RHand")

        time.sleep(1)

        #end position of the arm
        self.motion.setAngles("RShoulderPitch", 1.7, 0.1)

        time.sleep(4)

        #raise hand before sitting so no collision with leg
        self.motion.setAngles("RElbowRoll", 1.54, 0.2)
        self.motion.setAngles("RShoulderPitch", 1.0, 0.2)
        time.sleep(0.15)
        self.posture.goToPosture("Sit", 0.5)

    def two_fractions(self):
        #HANDS CURRENTLY DO NOT OPEN
        #moving the right hand to the beginning position
        self.motion.setAngles("RShoulderRoll", -0.5, 0.25)
        self.motion.setAngles("RShoulderPitch", 0.4, 0.25)
        self.motion.setAngles("RElbowRoll", 1.2, 0.25)
        self.motion.setAngles("RElbowYaw", 1.7, 0.25)
        self.motion.setAngles("RWristYaw", 1.5, 0.25)

        time.sleep(0.8)

        #emphasize the right hand
        self.motion.setAngles("RElbowRoll", 0.2, 0.2)

        time.sleep(0.3)

        #moving the left hand to the beginning position
        self.motion.setAngles("LShoulderRoll", 0.5, 0.25)
        self.motion.setAngles("LShoulderPitch", 0.4, 0.25)
        self.motion.setAngles("LElbowRoll", -1.2, 0.25)
        self.motion.setAngles("LElbowYaw", -1.7, 0.25)
        self.motion.setAngles("LWristYaw", -1.5, 0.25)

        time.sleep(0.8)

        #emphasize the left hand
        self.motion.setAngles("LElbowRoll", -0.2, 0.2)

        time.sleep(2.5)

        self.posture.goToPosture("Sit", 0.5)

    def look(self):
        self.genSpeech("i am now sitting")

    def sit(self):
        self.posture.goToPosture("Sit", 0.5)

    def left_relaxed_sit(self):
        self.genSpeech("i am now sitting")

    def right_relaxed_sit(self):
        self.genSpeech("i am now sitting")

    def numerator(self):
        self.genSpeech("i am now sitting")

    def denominator(self):
        self.genSpeech("i am now sitting")

    def etc(self):
        self.genSpeech("i am now sitting")

    def conversion(self):
        self.genSpeech("i am now sitting")

    def tilt(self):
        #this bit of code makes the robot tilt its head
        self.posture.goToPosture("Sit", 1.0)
        self.motion.setStiffnesses("Head", 1.0)
        self.genSpeech("i am now sitting")
        time.sleep(0.5)
        self.genSpeech("now i will tilt my head")
        time.sleep(3)

        #tilt head
        self.motion.setAngles("HeadPitch", 0.2, 0.2)
        time.sleep(1.5)
        self.genSpeech("hmmm. maybe you should try a little more before asking for a hint")

        #move back to the original position
        time.sleep(8)
        self.posture.goToPosture("Sit", 1.0)

    def hands(self):
        #this bit of code makes the robot put its hands together and head down
        self.posture.goToPosture("Sit", 0.5)
        self.motion.setStiffnesses("Head", 1.0)
        self.genSpeech("i am now sitting")
        time.sleep(0.5)
        self.genSpeech("now i will put my hands together and tilt down my head")
        time.sleep(5)

        #hands together and head down
        #self.motion.openHand("LHand")
        #self.motion.openHand("RHand")
        #self.motion.setAngles("RShoulderPitch", 1.0, 0.5)
        self.motion.setAngles("LShoulderRoll", -0.05, 0.25)
        self.motion.setAngles("RShoulderRoll", 0.05, 0.25)
        self.motion.setAngles("HeadPitch", 0.25, 0.15)
        time.sleep(3.5)
        self.genSpeech("hmmm. maybe try asking for a hint")

        #move back to the original position
        time.sleep(8)
        self.posture.goToPosture("Sit", 0.5)

    def breathe(self):
        self.posture.goToPosture("Stand", 1.0)
        #self.motion.setBreathEnabled("Body", True)

    def assess(self, what): #should we take the time.sleep() out since we are waiting using post?
        if(what is "correct"):
            randnr = random.randint(0,len(self.right)-1)
            id = self.genSpeech(self.right[randnr])
            time.sleep(3)
        elif(what is "wrong"):
            randnr = random.randint(0,len(self.wrong_postfix)-1)
            id = self.genSpeech(self.wrong_postfix[randnr])
            time.sleep(3)
        elif(what is "trouble"):
            randnr = random.randint(0,len(self.trouble)-1)
            id = self.genSpeech(self.trouble[randnr])
            time.sleep(3)
        elif(what is "hint"): 
            randnr = random.randint(0,len(self.hint)-1)
            id = self.genSpeech(self.hint[randnr])
            time.sleep(3)
        elif(what is "confused"):
            randnr = random.randint(0,len(self.confused)-1)
            id = self.genSpeech(self.confused[randnr])
            time.sleep(3)
        elif(what is "auto_hint"):
            randnr = random.randint(0,len(self.auto_hint)-1)
            id = self.genSpeech(self.auto_hint[randnr])
            time.sleep(3)
        return id



    def ask(self, question):
        self.genSpeech(question)
        time.sleep(2)

   
    def releaseNao(self):
        try:
            self.posture.goToPosture("SitRelax", 1.0)
            self.motion.stiffnessInterpolation("Body",0.0,self.stiffness)
        except Exception, e:
            print "Error when sitting down nao and making nao unstiff: "+str(e)
