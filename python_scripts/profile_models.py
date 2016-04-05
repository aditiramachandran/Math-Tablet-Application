import time


class Session:
    '''
    A session is a list of questions with the following properties:

    Properties:
        session_num: Integer representing session number
        pid: Integer representing user pid
    '''

    def __init__(self, questions=[], session_num=-1, pid=-1):
        self.session_num = session_num
        self.pid = pid
        super(Session, self).__init__(questions)

    def __repr__(self):
        return "Session(pid=%r, session_num=%r, questions=\\\n%s)" % \
            (self.pid, self.session_num, pformat(list(self)))


class Question:
    '''
    A Question contains live information about question being answered

    Properties:
        question_num: Integer representing question number in current session
        attempts: Integer representing number of attempts made at question (max 5)
        hints: Integer representing number of hints given (max 3)
        correct: Boolean representing whether or not question was eventually answered correctly
        total_time: Float representing total time, in seconds, that was spent on question
        hint_times: Array of Floats representing time (from start) when hint was given
            Note: -1 means that hint was not given
            [24.3, 59.6, -1]:
                hint1 given 24.3 seconds after start
                hint2 given 59.6 seconds after start
                hint3 not given
        attempt_times: Array of Floats representing time (from start) when attempt was made
            Note: -1 means that attempt was never made
            [35.4, 75.1, -1, -1, -1]:
                attempt1 made 35.4 seconds after start
                attempt2 made 75.1 seconds after start
                attempt3/4/5 never made


    '''
    def __init__(self, question_num=-1, attempts=0, hints=0, correct=False,
                 total_time=0.0, hint_times=[], attempt_times=[]):
        self.question_num = question_num
        self.attempts = attempts
        self.hints = hints
        self.correct = correct
        self.total_time = total_time
        self.hint_times = hint_times
        self.attempt_times = attempt_times

        # private vars for internal use
        self.__start_time = time.time()
        self.__elapsed_time = time.time()


    def question(self):

    def event_handler(self, msg_type, ):
        '''
        Handles question events and calls appropriate method
        '''

        if msgType == 'Q':
             self.__question() # = 'QUESTION'
        elif msgType == 'CA':
             self.__correct() # = 'CORRECT'
        elif msgType == 'IA':
             self.__incorrect()# = 'INCORRECT'
        elif msgType == 'LIA':
             self.__last_incorrect()# = 'LAST INCORRECT'
        elif msgType == 'H1':
             self.__hint(1)# = 'HINT 1'
        elif msgType == 'H2':
             self.__hint(2)# = 'HINT 2'
        elif msgType == 'H3':
             self.__hint(3)# = 'HINT 3'
        elif msgType == 'AH':
             self.__special(msgType) # = 'AUTOMATIC HINT'
        elif msgType == 'DH':
             self.__special(msgType) # = 'DENIED HINT'
        elif msgType == 'RS':
             # = 'ROBOT SPEECH'
        elif msgType == 'RA':
             # = 'ROBOT ACTION'
        else:

        return

