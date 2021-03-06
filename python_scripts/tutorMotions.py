import random
import time

import pdb
import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior
import almath

BASEPATH = "/home/nao/behaviors/"

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
        self.question_intro = anim.question_intro
        self.connectNao()

    def connectNao(self):
        # FRAME MANAGER FOR CALLING BEHAVIORS
        try:
            print 'in connect nao, host and port are:', self.host, ',', self.port
            self.frame = ALProxy("ALFrameManager", self.host, self.port)
        except Exception, e:
            print "Error when creating frame manager device proxy:"+str(e)
            exit(1)
        # POSTURE MANAGER#
        try:
            self.posture = postureProxy = ALProxy("ALRobotPosture", self.host, self.port)
        except Exception, e:
            print "Error creating posture proxy"+str(e)
            exit(1)

        # MOTION DEVICE FOR MOVEMENTS
        try:
            self.motion = ALProxy("ALMotion", self.host, self.port)
        except Exception, e:
            print "Error when creating motion device proxy:"+str(e)
            exit(1)

        # MAKE NAO STIFF (OTHERWISE IT WON'T MOVE)
        self.motion.stiffnessInterpolation("Body", self.stiffness, 1.0)

        # MOTION DEVICE FOR MOVEMENTS
        try:
            self.led = ALProxy("ALLeds", self.host, self.port)
        except Exception, e:
            print "Error when creating led proxy:"+str(e)
            exit(1)

        # CONNECT TO A SPEECH PROXY
        try:
            self.speechDevice = ALProxy("ALTextToSpeech", self.host, self.port)
        except Exception, e:
            print "Error when creating speech device proxy:"+str(e)
            exit(1)
        # bring to sitting position
        self.posture.goToPosture("Sit", 0.15)

    def genSpeech(self, sentence):
        try:
            # self.look()
            id = self.speechDevice.post.say(sentence)
            return id
        except Exception, e:
            print "Error when saying a sentence: "+str(e)

    def send_command(self, doBehavior):
        gesture_path = BASEPATH + doBehavior
        gesture_id = self.frame.newBehaviorFromFile(gesture_path, "")
        self.frame.playBehavior(gesture_id)
        self.frame.completeBehavior(gesture_id)

    def goodbye(self):
        self.genSpeech(anim.finish)
        time.sleep(5)
        self.bring_to_sit(1.0)

    def session_intro(self, sessionNum):
        # print sessionNum
        welcomePhrase = ''
        if sessionNum == 1:
            welcomePhrase = "Hello! My name is Nao. I am your personal robot tutor!"
        elif sessionNum == 2:
            welcomePhrase = "Welcome back!"
        elif sessionNum == 3:
            welcomePhrase = "Nice to see you again!"
        elif sessionNum == 4:
            welcomePhrase = "Hello again! Today is our last session."

        self.genSpeech(welcomePhrase)
        self.look()
        self.wave()
        self.look()

        if sessionNum == 1:
            self.genSpeech("I'm here to help you with some fractions problems today.")
            self.genSpeech("For each session, I have put the math problems on the tablet in front of you.")
            self.genSpeech("If you need any help, you can ask me by pressing the hint buttons at the bottom of each screen.")
            id = self.genSpeech("Great! Now let's work on some questions together!")
        elif sessionNum == 2:
            self.genSpeech("Just remember, if you need help on the problems, you can ask me by pressing the buttons on the bottom of the screen.")
            id = self.genSpeech("Let's get started!")
        elif sessionNum == 3:
            self.genSpeech("Let's try doing some more problems!")
            id = self.genSpeech("Remember to ask me for hints if you need them by using the buttons at the bottom of the screen.")
        elif sessionNum == 4:
            self.genSpeech("If you need help, the hint buttons are on the bottom of each screen.")
            id = self.genSpeech("Let's get started!")
        else:
            print "invalid sessionNum: no intro"
        # time.sleep(2)
        return id

    def intro(self):
        self.bring_to_sit(1.0)
        self.motion.setAngles("HeadPitch", -0.1, 0.5)
        self.led.fadeListRGB("FaceLeds", [0x00FFFFFF], [0.1])
        self.genSpeech("Hello! My name is Nao, your personal robot tutor.")
        self.genSpeech("I'm really excited to meet you and work on some problems together!")
        self.genSpeech("I hope you have a great session with me today!")
        # self.genSpeech("Have a great day, and I look forward to seeing you again soon!")
        self.wave()
        # self.genSpeech("Let's work on some fractions problems together.")
        # self.genSpeech("I'm going to put some problems on your tablet!")
        time.sleep(8)

    def move_head(self):
        # self.posture.goToPosture("Sit", 1.0)

        self.motion.setStiffnesses("Head", 1.0)
        # Example showing multiple trajectories
        # Interpolate the head yaw to 1.0 radian and back to zero in 2.0 seconds
        # while interpolating HeadPitch up and down over a longer period.
        # names  = ["HeadYaw", "HeadPitch"]
        names = ["HeadPitch"]
        # Each joint can have lists of different lengths, but the number of
        # angles and the number of times must be the same for each joint.
        # Here, the second joint ("HeadPitch") has three angles, and
        # three corresponding times.
        # angleLists  = [[50.0*almath.TO_RAD, 0.0],
        #           [-30.0*almath.TO_RAD, 30.0*almath.TO_RAD, 0.0]]
        angleLists = [-10.0*almath.TO_RAD, 20.0*almath.TO_RAD, 0.0]
        # timeLists   = [[1.0, 2.0], [ 1.0, 2.0, 3.0]]
        timeLists = [1.0, 2.0, 3.0]
        isAbsolute = True

        self.genSpeech("hello my name is nao")
        for j in range(5):
            self.motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)

            # time.sleep(1.0)
        # self.motion.setStiffnesses("Head", 0.0)

    def wave(self):
        self.motion.setAngles("RShoulderPitch", -1.0, 0.15)
        self.motion.setAngles("RShoulderRoll", -1.2, 0.15)
        self.motion.setAngles("RElbowRoll", 1.0, 0.1)
        self.motion.setAngles("RElbowYaw", 0.5, 0.1)
        self.motion.setAngles("RWristYaw", 0, 0.1)
        self.motion.openHand("RHand")

        time.sleep(0.7)

        # wave the hand 3 times, by moving the elbow
        for i in range(3):
            self.motion.setAngles("RElbowRoll", 1.5, 0.5)
            time.sleep(0.5)
            self.motion.setAngles("RElbowRoll", 0.5, 0.5)
            time.sleep(0.5)
        self.motion.setAngles("RElbowRoll", 1.0, 0.5)
        time.sleep(1)
        self.motion.closeHand("RHand")
        self.prepare_sit_right(0.15)
        time.sleep(4)
        self.bring_to_sit(1)

    def juddNelson(self):
        # this bit of code makes the robot thrust its right hand into the air
        self.bring_to_sit(0.5)
        time.sleep(0.1)
        # move to position
        self.motion.setAngles("RShoulderPitch", -1.0, 0.3)
        self.motion.setAngles("RShoulderRoll", -1.3, 0.3)
        self.motion.setAngles("RElbowRoll", 1.5, 0.3)
        self.motion.setAngles("RWristYaw", 0, 0.3)
        self.motion.closeHand("RHand")
        time.sleep(0.1)
        # time.sleep(1.0)
        # self.genSpeech("good job! that's correct!")
        self.motion.setAngles("RShoulderRoll", -1.0, 0.25)
        self.motion.setAngles("RElbowRoll", 1.0, 0.5)
        time.sleep(1.5)
        self.motion.setAngles("RShoulderRoll", -0.3, 0.15)
        self.motion.setAngles("RShoulderPitch", 1, 0.15)
        time.sleep(2)
        self.prepare_sit_right(0.15)

    def juddNelson_left(self):
        # this bit of code makes the robot thrust its left hand into the air
        # start in sitting position
        self.bring_to_sit(0.5)
        time.sleep(0.1)
        # move to position
        self.motion.setAngles("LShoulderPitch", -1.0, 0.3)
        self.motion.setAngles("LShoulderRoll", 1.3, 0.3)
        self.motion.setAngles("LElbowRoll", -1.5, 0.3)
        self.motion.setAngles("LWristYaw", 0, 0.3)
        self.motion.closeHand("LHand")
        time.sleep(0.1)
        # pump fist upward
        self.motion.setAngles("LShoulderRoll", 1.0, 0.25)
        self.motion.setAngles("LElbowRoll", -1.0, 0.5)

        time.sleep(1.5)
        self.motion.setAngles("LShoulderRoll", 0.3, 0.15)
        self.motion.setAngles("LShoulderPitch", 1, 0.15)
        time.sleep(2)
        self.prepare_sit_left(0.15)
        time.sleep(2)
        # return to sitting position
        self.bring_to_sit(1.0)

    def nod(self):
        # this bit of code makes the robot nod its head
        # self.posture.goToPosture("Sit", 0.5)
        self.motion.setStiffnesses("Head", 1.0)
        time.sleep(0.5)

        # move head
        # self.motion.setAngles("HeadPitch", 0, 0.5)
        # time.sleep(0.5)
        self.motion.setAngles("HeadPitch", 0.15, 0.25)
        time.sleep(0.5)
        self.motion.setAngles("HeadPitch", 0, 0.25)
        time.sleep(0.5)
        self.motion.setAngles("HeadPitch", 0.15, 0.25)
        # time.sleep(0.5)
        # self.genSpeech("yes, that's correct. good job!")

        # move back to original position
        time.sleep(3)
        self.bring_to_sit(1.0)

    def shake(self):
        # this bit of code makes the robot shake its head
        # self.posture.goToPosture("Sit", 0.5)
        self.motion.setStiffnesses("Head", 1.0)
        # time.sleep(0.5)

        # shake head
        self.motion.setAngles("HeadPitch", 0, 0.05)
        # self.motion.setAngles("HeadYaw", 0, 0.05)
        # time.sleep(0.5)
        self.motion.setAngles("HeadYaw", -0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", 0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", -0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", 0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", 0, 0.3)

        time.sleep(1)
        self.look()
        time.sleep(0.5)
        self.bring_to_sit(1.0)

    def last_shake(self):
        # this bit of code makes the robot shake its head
        # self.posture.goToPosture("Sit", 0.5)
        self.motion.setStiffnesses("Head", 1.0)
        time.sleep(0.5)

        # shake head
        self.motion.setAngles("HeadPitch", 0, 0.3)
        for i in range(2):
            time.sleep(0.5)
            self.motion.setAngles("HeadYaw", -0.5, 0.3)
            time.sleep(0.5)
            self.motion.setAngles("HeadYaw", 0.5, 0.3)
        time.sleep(0.5)
        self.motion.setAngles("HeadYaw", 0, 0.3)

        # move back to the original position
        time.sleep(2.5)
        self.bring_to_sit(1.0)

    def scale_up(self):
        # start position of the arm
        # self.motion.setAngles("HeadPitch", 0, 0.15)
        self.motion.setAngles("RShoulderPitch", 0.4, 0.1)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.1)
        self.motion.setAngles("RElbowYaw", 1.5, 0.1)
        self.motion.setAngles("RElbowRoll", 0.4, 0.1)
        self.motion.setAngles("RWristYaw", 1.6, 0.1)
        self.motion.openHand("RHand")

        # time.sleep(0.3)

        # end position of the arm
        self.motion.setAngles("RShoulderPitch", 0.4, 0.3)
        self.motion.setAngles("RElbowRoll", 1.3, 0.3)

        time.sleep(2)
        self.bring_to_sit(0.15)
        time.sleep(2)

    def scale_down(self):
        # start position of the arm
        # self.motion.setAngles("HeadPitch", 0, 0.15)
        self.motion.setAngles("RShoulderPitch", 0.7, 0.2)
        self.motion.setAngles("RShoulderRoll", -1.2, 0.2)
        self.motion.setAngles("RElbowYaw", 1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 1.4, 0.2)
        self.motion.setAngles("RWristYaw", 0, 0.2)
        self.motion.openHand("RHand")

        # time.sleep(0.3)

        # end position of the arm
        self.motion.setAngles("RShoulderPitch", 1.5, 0.1)

        time.sleep(2.5)
        self.bring_to_sit(0.15)
        time.sleep(2)

    def scale_down_left(self):
        # start position of the arm
        # self.motion.setAngles("HeadPitch", 0, 0.15)
        self.motion.setAngles("LShoulderPitch", 0.7, 0.2)
        self.motion.setAngles("LShoulderRoll", 1.2, 0.2)
        self.motion.setAngles("LElbowYaw", -1.5, 0.2)
        self.motion.setAngles("LElbowRoll", -1.4, 0.2)
        self.motion.setAngles("LWristYaw", 0, 0.2)
        self.motion.openHand("LHand")

        # time.sleep(0.3)

        # end position of the arm
        self.motion.setAngles("LShoulderPitch", 1.5, 0.1)

        time.sleep(2.5)
        self.prepare_sit_left(0.15)
        time.sleep(2)

    def two_fractions(self):
        # moving the right hand to the beginning position
        self.motion.setAngles("HeadPitch", 0, 0.15)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RShoulderPitch", 0.4, 0.2)
        self.motion.setAngles("RElbowRoll", 1.2, 0.2)
        self.motion.setAngles("RElbowYaw", 1.7, 0.2)
        self.motion.setAngles("RWristYaw", 1.5, 0.2)

        time.sleep(0.6)

        # emphasize the right hand
        self.motion.setAngles("HeadYaw", -0.7, 0.2)
        self.motion.setAngles("RElbowRoll", 0.2, 0.2)

        time.sleep(0.2)

        # moving the left hand to the beginning position
        self.motion.setAngles("LShoulderRoll", 0.5, 0.25)
        self.motion.setAngles("LShoulderPitch", 0.4, 0.25)
        self.motion.setAngles("LElbowRoll", -1.2, 0.25)
        self.motion.setAngles("LElbowYaw", -1.7, 0.25)
        self.motion.setAngles("LWristYaw", -1.5, 0.25)

        time.sleep(0.6)

        # emphasize the left hand
        self.motion.setAngles("HeadYaw", 0.7, 0.2)
        self.motion.setAngles("LElbowRoll", -0.2, 0.2)

        # open both hands and move the head back center
        self.motion.openHand("RHand")
        self.motion.setAngles("HeadYaw", 0, 0.05)
        self.motion.openHand("LHand")

        time.sleep(0.6)

        # bring arms in to avoid scooching sit
        self.motion.setAngles("RShoulderRoll", -0.15, 0.2)
        self.motion.setAngles("LShoulderRoll", 0.15, 0.2)
        self.motion.setAngles("RElbowYaw", 0, 0.2)
        self.motion.setAngles("LElbowYaw", 0, 0.2)
        self.motion.setAngles("LElbowRoll", -1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 1.5, 0.2)
        time.sleep(1)

        self.bring_to_sit(0.5)

    # used for word problems
    def two_hands(self):
        time.sleep(9)

        # moving the right hand to the beginning position
        self.motion.setAngles("HeadPitch", 0, 0.15)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RShoulderPitch", 0.4, 0.2)
        self.motion.setAngles("RElbowRoll", 1.2, 0.2)
        self.motion.setAngles("RElbowYaw", 1.7, 0.2)
        self.motion.setAngles("RWristYaw", 1.5, 0.2)

        # moving the left hand to the beginning position
        self.motion.setAngles("LShoulderRoll", 0.5, 0.25)
        self.motion.setAngles("LShoulderPitch", 0.4, 0.25)
        self.motion.setAngles("LElbowRoll", -1.2, 0.25)
        self.motion.setAngles("LElbowYaw", -1.7, 0.25)
        self.motion.setAngles("LWristYaw", -1.5, 0.25)

        time.sleep(0.8)

        # emphasize the right hand
        # self.motion.setAngles("HeadYaw", -0.7, 0.2)
        self.motion.setAngles("RElbowRoll", 0.2, 0.2)

        # time.sleep(0.3)

        # emphasize the left hand
        # self.motion.setAngles("HeadYaw", 0.7, 0.2)
        self.motion.setAngles("LElbowRoll", -0.2, 0.2)

        # open both hands and move the head back center
        self.motion.openHand("RHand")
        self.motion.setAngles("HeadYaw", 0, 0.05)
        self.motion.openHand("LHand")

        time.sleep(0.5)

        # bring arms in to avoid scooching sit
        self.motion.setAngles("RShoulderRoll", -0.15, 0.2)
        self.motion.setAngles("LShoulderRoll", 0.15, 0.2)
        self.motion.setAngles("RElbowYaw", 0, 0.2)
        self.motion.setAngles("LElbowYaw", 0, 0.2)
        self.motion.setAngles("LElbowRoll", -1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 1.5, 0.2)
        time.sleep(1)

        self.bring_to_sit(0.5)

    def multiples(self):
        # moving the right hand to the beginning position
        self.motion.setAngles("HeadPitch", 0, 0.15)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RShoulderPitch", 0.4, 0.2)
        self.motion.setAngles("RElbowRoll", 1.2, 0.2)
        self.motion.setAngles("RElbowYaw", 1.7, 0.2)
        self.motion.setAngles("RWristYaw", 1.5, 0.2)

        time.sleep(0.8)

        # emphasize the right hand
        self.motion.setAngles("HeadYaw", -0.7, 0.2)
        self.motion.setAngles("RElbowRoll", 0.2, 0.2)

        time.sleep(2.5)

        # moving the left hand to the beginning position
        self.motion.setAngles("LShoulderRoll", 0.5, 0.25)
        self.motion.setAngles("LShoulderPitch", 0.4, 0.25)
        self.motion.setAngles("LElbowRoll", -1.2, 0.25)
        self.motion.setAngles("LElbowYaw", -1.7, 0.25)
        self.motion.setAngles("LWristYaw", -1.5, 0.25)

        time.sleep(0.8)

        # emphasize the left hand
        self.motion.setAngles("HeadYaw", 0.7, 0.2)
        self.motion.setAngles("LElbowRoll", -0.2, 0.2)

        # wait to bring hands together
        # time.sleep(2)

        # open both hands and move the head back center
        self.motion.openHand("RHand")
        self.motion.setAngles("HeadYaw", 0, 0.05)
        self.motion.openHand("LHand")

        time.sleep(0.9)

        # bring arms in to avoid scooching sit
        self.motion.setAngles("RShoulderRoll", -0.15, 0.2)
        self.motion.setAngles("LShoulderRoll", 0.15, 0.2)
        self.motion.setAngles("RElbowYaw", 0, 0.2)
        self.motion.setAngles("LElbowYaw", 0, 0.2)
        self.motion.setAngles("LElbowRoll", -1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 1.5, 0.2)
        time.sleep(1)

        self.bring_to_sit(0.5)

    def look(self):
        # head looking at student and talking, for right handers
        # CAN I REMOVE THIS
        # self.posture.goToPosture("Sit", 0.2)
        self.motion.setAngles("HeadYaw", -0.25, 0.1)
        self.motion.setAngles("HeadPitch", 0.15, 0.1)

    def look_left(self):
        # head looking at student and talking, for left handers
        self.motion.setAngles("HeadYaw", 0.25, 0.1)
        self.motion.setAngles("HeadPitch", 0.15, 0.1)

    def sit(self):
        # self.posture.goToPosture("Sit", 0.2)
        # head looks down at tablet, for right handers
        self.motion.setAngles("HeadYaw", 0.3, 0.1)
        self.motion.setAngles("HeadPitch", 0.37, 0.1)
        # self.motion.setAngles("HeadYaw", 0.25, 0.15)

    def sit_left(self):
        # head looks down at tablet, for left handers
        self.motion.setAngles("HeadYaw", 0, 0.1)
        self.motion.setAngles("HeadPitch", 0.33, 0.1)

    def left_relaxed_sit(self):
        # move the left hand up and out of the way to avoid collision
        self.motion.setAngles("HeadPitch", 0.3, 0.15)
        self.motion.setAngles("LShoulderPitch", 0.5, 0.2)
        self.motion.setAngles("LShoulderRoll", 0.5, 0.2)
        self.motion.setAngles("LElbowRoll", -0.1, 0.2)

        time.sleep(1)

        # move hand around to the side
        self.motion.setAngles("LShoulderPitch", 1.8, 0.2)
        self.motion.setAngles("LShoulderRoll", 0.5, 0.2)

        time.sleep(0.5)

        # adjust elbow inward
        self.motion.setAngles("LElbowRoll", -1.1, 0.2)

        # adjust shoulder accordingly
        self.motion.setAngles("LShoulderRoll", 0.2, 0.2)

        time.sleep(5)

        # backtrack motions to prevent collision with leg
        self.motion.setAngles("LShoulderRoll", 0.5, 0.2)
        time.sleep(0.1)
        self.motion.setAngles("LElbowRoll", -0.1, 0.2)
        self.motion.setAngles("LShoulderPitch", 0.5, 0.2)

        time.sleep(0.5)

        self.bring_to_sit(0.5)
        self.motion.setAngles("HeadPitch", 0.3, 0.15)

    def right_relaxed_sit(self):
        # move the right hand up and out of the way to avoid collision
        self.motion.setAngles("HeadPitch", 0.3, 0.15)
        self.motion.setAngles("RShoulderPitch", 0.5, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RElbowRoll", 0.1, 0.2)

        time.sleep(1)

        # move hand around to the side
        self.motion.setAngles("RShoulderPitch", 1.8, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)

        time.sleep(0.5)

        # adjust elbow inward
        self.motion.setAngles("RElbowRoll", 1.1, 0.2)

        # adjust shoulder accordingly
        self.motion.setAngles("RShoulderRoll", -0.2, 0.2)

        time.sleep(5)

        # backtrack motions to prevent collision with leg
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        time.sleep(0.1)
        self.motion.setAngles("RElbowRoll", 0.1, 0.2)
        self.motion.setAngles("RShoulderPitch", 0.5, 0.2)

        time.sleep(0.5)

        self.bring_to_sit(0.5)
        self.motion.setAngles("HeadPitch", 0.3, 0.15)

    def numerator(self):
        # self.posture.goToPosture("Sit", 0.5)

        # start position of the arm
        # self.motion.setAngles("HeadPitch", 0, 0.15)
        self.motion.setAngles("RShoulderPitch", -0.3, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RElbowYaw", 1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 0.4, 0.2)
        self.motion.setAngles("RWristYaw", 1.6, 0.2)
        self.motion.openHand("RHand")

        time.sleep(2)
        self.prepare_sit_right()
        time.sleep(2)

    def denominator(self):
        # self.posture.goToPosture("Sit", 0.5)

        # start position of the arm
        # self.motion.setAngles("HeadPitch", 0, 0.15)
        self.motion.setAngles("RShoulderPitch", 0.8, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RElbowYaw", 1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 0.4, 0.2)
        self.motion.setAngles("RWristYaw", 1.6, 0.2)
        self.motion.openHand("RHand")

        time.sleep(2)

        # raise up elbow to avoid collision
        self.motion.setAngles("RElbowRoll", 0.8, 0.2)
        self.motion.setAngles("RWristYaw", 1.3, 0.2)

        self.prepare_sit_right(0.15)

    def numerator_denominator(self):
        # start position of the arm
        # self.motion.setAngles("HeadPitch", 0, 0.15)

        time.sleep(2.5)

        self.motion.setAngles("RShoulderPitch", -0.3, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RElbowYaw", 1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 0.4, 0.2)
        self.motion.setAngles("RWristYaw", 1.6, 0.2)
        self.motion.openHand("RHand")

        time.sleep(0.3)

        self.motion.setAngles("RShoulderPitch", 0.8, 0.2)
        self.motion.setAngles("RShoulderRoll", -0.5, 0.2)
        self.motion.setAngles("RElbowYaw", 1.5, 0.2)
        self.motion.setAngles("RElbowRoll", 0.4, 0.2)
        self.motion.setAngles("RWristYaw", 1.6, 0.2)
        self.motion.openHand("RHand")

        time.sleep(0.5)
        self.prepare_sit_right()
        time.sleep(2)

    def etc(self):
        # head faces straight
        self.motion.setAngles("HeadPitch", 0, 0.15)

        time.sleep(0.25)

        # start position of the arm
        self.motion.setAngles("LShoulderRoll", 0.3, 0.25)
        self.motion.setAngles("LShoulderPitch", 0.4, 0.25)
        self.motion.setAngles("LElbowRoll", -1.2, 0.25)
        self.motion.setAngles("LElbowYaw", -1.7, 0.25)
        self.motion.setAngles("LWristYaw", -1.5, 0.25)

        time.sleep(0.8)

        # emphasize the left hand
        self.motion.setAngles("HeadYaw", 0.2, 0.2)
        self.motion.setAngles("LElbowRoll", -0.2, 0.2)
        self.motion.openHand("LHand")

        time.sleep(2)

        self.bring_to_sit(0.5)

    def point_question(self):
        # move left hand to point to tablet
        time.sleep(3.5)
        self.motion.setAngles("LShoulderRoll", 0.3, 0.25)
        self.motion.setAngles("LShoulderPitch", 0.4, 0.25)
        self.motion.setAngles("LElbowRoll", -0.2, 0.25)
        self.motion.setAngles("LElbowYaw", -1.7, 0.25)
        self.motion.setAngles("LWristYaw", -1.5, 0.25)

        self.motion.openHand("LHand")

        # look at the tablet/left hand?
        # self.motion.setAngles("HeadYaw", 0.2, 0.2)
        # Bring back to sit
        time.sleep(2)
        self.prepare_sit_left(0.15)
        time.sleep(2)

        time.sleep(1.5)
        self.bring_to_sit(0.5)

    def conversion(self):
        # head faces straight
        # self.motion.setAngles("HeadPitch", 0, 0.15)

        # move left hand to represent the denominator
        self.motion.setAngles("LShoulderPitch", 0.7, 0.15)
        self.motion.setAngles("LShoulderRoll", 0.15, 0.1)
        self.motion.openHand("LHand")

        time.sleep(0.2)

        # move right hand to represent the whole number
        self.motion.setAngles("RShoulderRoll", -0.35, 0.2)
        self.motion.setAngles("RShoulderPitch", 0.4, 0.2)
        # bring elbow in
        self.motion.setAngles("RElbowRoll", 1.2, 0.2)
        self.motion.openHand("RHand")

        time.sleep(0.2)

        # move left hand to represent the numerator
        self.motion.setAngles("LShoulderPitch", -0.05, 0.2)

        time.sleep(3)
        self.bring_to_sit(0.5)

    def congratulations(self):
        # this bit of code makes the robot thrust its right hand into the air
        # start in sitting position
        # self.posture.goToPosture("Sit", 0.5)
        # time.sleep(0.1)
        # move to position
        self.motion.closeHand("LHand")
        self.motion.setAngles("RShoulderPitch", -1.0, 0.3)
        self.motion.setAngles("RShoulderRoll", -1.3, 0.3)
        self.motion.setAngles("RElbowRoll", 1.5, 0.3)
        self.motion.setAngles("RWristYaw", 0, 0.3)
        self.motion.setAngles("LShoulderPitch", -1.0, 0.3)
        self.motion.setAngles("LShoulderRoll", 1.3, 0.3)
        self.motion.setAngles("LElbowRoll", -1.5, 0.3)
        self.motion.setAngles("LWristYaw", 0, 0.3)
        self.motion.closeHand("RHand")

        time.sleep(0.1)
        # time.sleep(1.0)
        # self.genSpeech("good job! that's correct!")
        self.motion.setAngles("RShoulderRoll", -1.0, 0.25)
        self.motion.setAngles("RElbowRoll", 1.0, 0.5)
        self.motion.setAngles("LShoulderRoll", 1.0, 0.25)
        self.motion.setAngles("LElbowRoll", -1.0, 0.5)
        """
        time.sleep(0.4)
        self.motion.setAngles("RShoulderRoll", -1.3, 0.3)
        self.motion.setAngles("RElbowRoll", 1.5, 0.3)
        self.motion.setAngles("LShoulderRoll", 1.3, 0.3)
        self.motion.setAngles("LElbowRoll", -1.5, 0.3)
        time.sleep(0.2)
        self.motion.setAngles("RShoulderRoll", -1.0, 0.25)
        self.motion.setAngles("RElbowRoll", 1.0, 0.5)
        self.motion.setAngles("LShoulderRoll", 1.0, 0.25)
        self.motion.setAngles("LElbowRoll", -1.0, 0.5)
        time.sleep(0.4)
        self.motion.setAngles("RShoulderRoll", -1.3, 0.3)
        self.motion.setAngles("RElbowRoll", 1.5, 0.3)
        self.motion.setAngles("LShoulderRoll", 1.3, 0.3)
        self.motion.setAngles("LElbowRoll", -1.5, 0.3)
        time.sleep(0.2)
        self.motion.setAngles("RShoulderRoll", -1.0, 0.25)
        self.motion.setAngles("RElbowRoll", 1.0, 0.5)
        self.motion.setAngles("LShoulderRoll", 1.0, 0.25)
        self.motion.setAngles("LElbowRoll", -1.0, 0.5)
        # self.genSpeech("yay you did it!")
        # time.sleep(2)
        # self.genSpeech("now i will put my hand back down")
        """
        # bring arms down to avoid drastic sit
        self.motion.setAngles("RShoulderPitch", 0.5, 0.2)
        self.motion.setAngles("LShoulderPitch", 0.5, 0.2)
        self.motion.setAngles("RShoulderRoll", 0, 0.2)
        self.motion.setAngles("LShoulderRoll", 0, 0.2)
        time.sleep(3)
        self.bring_to_sit(1.0)

    def tilt(self):
        # this bit of code makes the robot tilt its head
        self.bring_to_sit(1.0)
        self.motion.setStiffnesses("Head", 1.0)
        self.genSpeech("i am now sitting")
        time.sleep(0.5)
        self.genSpeech("now i will tilt my head")
        time.sleep(3)

        # tilt head
        self.motion.setAngles("HeadPitch", 0.2, 0.2)
        time.sleep(1.5)
        self.genSpeech("hmmm. maybe you should try a little more before asking for a hint")

        # move back to the original position
        time.sleep(8)
        self.bring_to_sit(0.5)

    def hands(self):
        # this bit of code makes the robot put its hands together and head down
        self.bring_to_sit(1.0)
        self.motion.setStiffnesses("Head", 1.0)
        self.genSpeech("i am now sitting")
        time.sleep(0.5)
        self.genSpeech("now i will put my hands together and tilt down my head")
        time.sleep(5)

        # hands together and head down
        # self.motion.openHand("LHand")
        # self.motion.openHand("RHand")
        # self.motion.setAngles("RShoulderPitch", 1.0, 0.5)
        self.motion.setAngles("LShoulderRoll", -0.05, 0.25)
        self.motion.setAngles("RShoulderRoll", 0.05, 0.25)
        self.motion.setAngles("HeadPitch", 0.25, 0.15)
        time.sleep(3.5)
        self.genSpeech("hmmm. maybe try asking for a hint")

        # move back to the original position
        time.sleep(8)
        self.bring_to_sit(0.5)

    def breathe(self):
        self.posture.goToPosture("Stand", 1.0)
        # self.motion.setBreathEnabled("Body", True)

    def assess(self, what):
        # should we take the time.sleep() out since we are waiting using post?
        if(what is "correct"):
            randnr = random.randint(0, len(self.right) - 1)
            speech = self.right[randnr]
            # time.sleep(3)
        elif(what is "wrong"):
            randnr = random.randint(0, len(self.wrong_postfix) - 1)
            speech = self.wrong_postfix[randnr]
            # time.sleep(3)
        elif(what is "trouble"):
            randnr = random.randint(0, len(self.trouble) - 1)
            speech = self.trouble[randnr]
            # time.sleep(3)
        elif(what is "hint"):
            randnr = random.randint(0, len(self.hint) - 1)
            speech = self.hint[randnr]
            # time.sleep(3)
        elif(what is "confused"):
            randnr = random.randint(0, len(self.confused) - 1)
            speech = self.confused[randnr]
            # time.sleep(3)
        elif(what is "auto_hint"):
            randnr = random.randint(0, len(self.auto_hint) - 1)
            speech = self.auto_hint[randnr]
            # time.sleep(3)
        id = self.genSpeech(speech)
        return [id, speech]

    # this function is now used to determine the intro movement
    def assessQuestion(self, what):
        # print what
        if(what == "Scaling Up"):
            # print "scaling up question, movement"
            self.scale_up()
            # time.sleep(3)
        elif(what == "Scaling Down"):
            self.scale_down_left()
            # time.sleep(3)
        elif(what == "Common Denominator"):
            self.point_question()
            # time.sleep(3)
        elif(what == "Conversion"):
            # UNSURE HERE
            self.point_question()
            # time.sleep(3)
        elif(what == "Adding Like Denominators Word Problem"):
            self.two_fractions()
            # time.sleep(3)
        elif(what == "Subtracting Like Denominators Word Problem"):
            self.two_fractions()
        elif(what == "Adding Like Denominators"):
            self.two_fractions()
            # time.sleep(3)
        elif(what == "Subtracting Like Denominators"):
            self.two_fractions()
        elif(what == "Adding Unlike Denominators Word Problem"):
            self.two_fractions()
            # time.sleep(3)
        elif(what == "Subtracting Unlike Denominators Word Problem"):
            self.two_fractions()
        elif(what == "Adding Unlike Denominators"):
            self.two_fractions()
            # time.sleep(3)
        elif(what == "Subtracting Unlike Denominators"):
            self.two_fractions()
            # time.sleep(3)

    def introQuestion(self, what):
        randnr = random.randint(0, len(self.question_intro) - 1)
        speech = self.question_intro[randnr]
        speech = speech + what + ". Here it is!"
        id = self.genSpeech(speech)
        return [id, speech]

    def assessHint2(self, what):
        if (what == "Scaling Up"):
            self.numerator_denominator()
            time.sleep(1)
        elif (what == "Scaling Down"):
            self.numerator_denominator()
            time.sleep(1)

    def assessHint3(self, what):
        if(what == "Conversion"):
            self.conversion()
            time.sleep(1)
        elif (what == "Common Denominator"):
            time.sleep(4)
            self.multiples()
            time.sleep(1)

    def ask(self, question):
        self.genSpeech(question)
        time.sleep(2)

    # call before bringing to sit to avoid scooching sit, if the only motions away from sit were using arm joints
    # essentially the same as self.posture.goToPosture("Sit", 0.15), except this won't move the legs
    # uses the angle settings from ALMotionProxy::getSummary() when the robot is in a sitting position, rounded to 2nd decimal
    def prepare_sit_right(self, speed):
        self.motion.setAngles("RShoulderRoll", -0.27, speed)
        self.motion.setAngles("RShoulderPitch", 0.919, speed)
        self.motion.setAngles("RElbowRoll", 1.25, speed)
        self.motion.setAngles("RElbowYaw", 0.5, speed)
        self.motion.setAngles("RWristYaw", 0.01, speed)

    def prepare_sit_left(self, speed):
        self.motion.setAngles("LShoulderRoll", 0.26, speed)
        self.motion.setAngles("LShoulderPitch", 0.885, speed)
        self.motion.setAngles("LElbowRoll", -1.2, speed)
        self.motion.setAngles("LElbowYaw", -.466, speed)
        self.motion.setAngles("LWristYaw", -0.006, speed)

    def bring_to_sit(self, speed=0.15):
        self.prepare_sit_right(speed)
        self.prepare_sit_left(speed)

    def releaseNao(self):
        try:
            self.posture.goToPosture("SitRelax", 1.0)
            self.motion.stiffnessInterpolation("Body", 0.0, self.stiffness)
        except Exception, e:
            print "Error when sitting down nao and making nao unstiff: "+str(e)
