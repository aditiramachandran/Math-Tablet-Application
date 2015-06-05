import os
import os.path
import sys
import random
import time
import datetime
import collections
import socket
sys.path.append('/Users/aditi/python_libs_nao')

import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior    

from tutorMotions import *

class TutoringSession:
	def __init__(self, host, port, goNao):
		self.host = host
		self.port = port
		self.goNao = goNao
		self.numHintRequests = 0
		self.numQuestions = 0
		self.numCorrect = 0
		self.numIncorrect = 0

	def log_answer(self,history,q_type,answer,correct):
		history.write("Type: %d, Answered: %s, %s\n"%(q_type,answer,correct))
		history.flush()

	def log_data(self,data,per,tot,cor):
		data.seek(0)
		data.truncate()
		data.write("%d\n"%per)
		data.write("%d\n"%tot)
		data.write("%d\n"%cor)

	#def tutor(history, data, categ):
	def tutor(self,categ):
		i = 1
		new = True
		wrong = []
		per = []
		tot = []
		cor = []
		print "num categories:", categ

		#then set up server connection for tablet to make connection
		BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((self.host, self.port))
		s.listen(1)
		print 'Waiting for client connection...'

		try:
			conn, addr = s.accept()
			print 'Connection address:', addr
			msg = conn.recv(BUFFER_SIZE)
			print msg
		except KeyboardInterrupt:
			sys.exit()

		while 1:
			try:
				msg = conn.recv(BUFFER_SIZE)
				if not msg: break
				print "received msg:", msg

				#parse message type to know what to do with it
				msgType = msg.split(":")[0]
				msg = msg.split(":")[1]

				robot_speech = msg.replace("=","").strip()
				robot_speech = "What does " + robot_speech + " equal?"

				if msgType == 'Q': #question
					self.numQuestions += 1
					if self.goNao is None:
						os.system("say " + robot_speech)

					else:
						self.goNao.genSpeech(robot_speech) 
				elif msgType == 'CA': #correct attempt
					self.numCorrect += 1
					print 'correct answer'
				elif msgType == 'IA': #incorrect attempt
					self.numIncorrect += 1
					print 'incorrect answer'
				elif msgType == 'H': #hint request
					self.numHintRequests += 1
					print 'hint request'
				else:
					print 'error: unknown message type'

			except KeyboardInterrupt:
				conn.close()
				sys.exit(0)


		"""
		for j in range(categ):
			wrong.append(0)
			if not data[j].readline():
				per.append(100)
				tot.append(0)
				cor.append(0)
			else:
				data[j].seek(0)
				per.append(int(data[j].readline()))
				tot.append(int(data[j].readline()))
				cor.append(int(data[j].readline()))

		#Anthony's question/answer parsing code - take parts from this and move it above
		while 1:
			msg = s.recv(BUFFER_SIZE)
			if not msg:
				break
			if (msg == "exit"):
				break
			q_type, help, answer, human_choice = msg.split(' ')
			q_type = int(q_type)
			help = int(help)
			answer = int(answer)
			human_choice = int(human_choice)

			correct = False
			tot[q_type] += 1

			if human_choice == answer:
				correct = True
				wrong[q_type] = 0
				cor[q_type] += 1
				goNao.assess("correct")

			elif help:
				tot[q_type] -= 1
				per[q_type] = (float(cor[q_type])/float(tot[q_type])) * 100
				
				if per[q_type] > 70:
					goNao.genSpeech("I think you can do it. Try to answer.")
				
				else:
					goNao.assess("hint")
			
			else:
				per[q_type] = (float(cor[q_type])/float(tot[q_type])) * 100
				wrong[q_type] = wrong[q_type] + 1
				
				if wrong[q_type] > 4:
					goNao.assess("trouble")
					break_choice = raw_input("Take a break? y for yes, n for no: ")
					if break_choice is "y":
						goNao.genSpeech("I have a fun game for you.")
						time.sleep(60) # play a game
						goNao.genSpeech("That was fun! Now let's get back to work.")
				
				elif per[q_type] < 70 and tot[q_type] > 10:
					goNao.assess("hint")
					hint_choice = raw_input("Would you like a hint? y for yes, n for no: ")
					if hint_choice is "y":
						goNao.genSpeech("I think I can help")
						# give a hint

				elif per[q_type] > 70 and tot[q_type] > 10:
					goNao.assess("confused")
				
				else:
					goNao.assess("wrong")

			log_answer(history,q_type,human_choice,correct)
		
		for i in range(categ):
			if tot[i] is not 0:
				per[i] = (float(cor[i])/float(tot[i])) * 100
			log_data(data[i],per[i],tot[i],cor[i])
		
		goNao.goodbye()
		"""


def main():
	#start main piece of nao tutoring interaction
	NAO_PORT = 9559
	useRobot = False
	if len(sys.argv) >= 3:
		TCP_IP = sys.argv[1]
		TCP_PORT = int(sys.argv[2])
		if len(sys.argv) == 4:
			if sys.argv[3]=='-robot':
				useRobot = True	
	
	if useRobot:
		#Get the Nao's IP from file
		try:
			ipFile = open("ip.txt")
			NAO_IP = ipFile.readline().replace("\n","").replace("\r","")
		except Exception as e:
			print "Could not open file ip.txt"
			NAO_IP = raw_input("Please write Nao's IP address. ") 
	print 'ip and port:', TCP_IP, TCP_PORT
	print 'nao ip:', NAO_IP


	#first connect to the NAO if -robot flag is set
	goNao = None
	if useRobot:
		try:
		    goNao = Gesture(NAO_IP, NAO_PORT)
		except Exception as e:
		    print "Could not find nao. Check that your ip is correct (%s)" %TCP_IP
		    sys.exit()


		#Set postureProxy
		try:
		    postureProxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
		except Exception, e:
		    print "Could not create proxy to ALRobotPosture"
		    print "Error was: ", e


	#Choose an action
	#Set all the possible commands
	commands=collections.OrderedDict((("i","Run the intro"),
	("r","Release motors"),
	("t","Test new code"),
	("s","Start tutoring interaction")
	))


	#Output all the commands
	print "\nPlease choose an action:"
	for key,value in commands.items():
	    print("\t%s => %s"%(key,value))


	#Have the user select the choice
	choice = ""
	if choice not in commands:
	    choice = raw_input('Choice: ').replace("\n","").replace("\r","")


	#Execute the user's choice
	if(choice == "i"):
	    postureProxy.goToPosture("Stand", 1.0)
	    goNao.intro()

	elif(choice=="r"):
	    goNao.releaseNao()

	elif(choice == "t"):
		history = open("data/Tony.txt","a")
		tutor(history)

	elif(choice == "s"):
		session = TutoringSession(TCP_IP, TCP_PORT, goNao)
		with open('topics.txt') as f:
			categ = sum(1 for _ in f)
		session.tutor(categ)

		"""
	    participant_name = raw_input('Input participant\'s name: ').replace("\n","").replace("\r","")
	    
	    with open('topics.txt') as f:
	    	categ = sum(1 for _ in f)
	    if categ != 2:
	    	print "Error"
	    	exit()

	    data = []
	    
	    if os.path.exists("data_TCP/%s.txt"%participant_name):
	    	history = open("data_TCP/%s.txt"%participant_name,"a")
	    
	    else:
	    	history = open("data_TCP/%s.txt"%participant_name,"a")
	    	history.write("%s\n"%participant_name)
	    	for i in range(categ):
	    		open("data_TCP/%s_%d.txt"%(participant_name,i),"w")
	    
	    history.write("------------\n")
	    today = datetime.datetime.now()
	    history.write("%s\n" % today)
	    history.flush()

	    for i in range(categ):
	    	data.append(open("data_TCP/%s_%d.txt"%(participant_name,i),"r+"))

	    #goNao.intro()
	    postureProxy.goToPosture("SitRelax", 1.0)

	    goNao.genSpeech("Shall we get started, %s?"%participant_name)
	    time.sleep(2)

	    tutor(history, data, categ)
	    postureProxy.goToPosture("SitRelax", 1.0)

	    goNao.releaseNao()
	    history.write("\n")
	    history.close()
	    """

if __name__ == "__main__": 
	main()

