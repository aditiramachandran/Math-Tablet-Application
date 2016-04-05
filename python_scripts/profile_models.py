import time
import pformat


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
        total_time: Float representing total time, in ms, that was spent on question
        hint_times: Array of Floats representing time (from start) when hint was given
            Note: -1 means that hint was not given
            [24.3, 59.6, -1]:
                hint1 given 24.3 ms after start
                hint2 given 59.6 ms after start
                hint3 not given
        attempt_times: Array of Floats representing time (from start) when attempt was made
            Note: -1 means that attempt was never made
            [35.4, 75.1, -1, -1, -1]:
                attempt1 made 35.4 ms after start
                attempt2 made 75.1 ms after start
                attempt3/4/5 never made
    '''
    MAX_HINTS = 3
    MAX_ATTEMPTS = 5

    def __init__(self, question_num=-1, attempts=0, hints=0, correct=False,
                 total_time=0.0, hint_times=[], attempt_times=[], complete=False):
        self.question_num = question_num
        self.attempts = attempts
        self.hints = hints
        self.correct = correct
        self.total_time = total_time
        self.hint_times = hint_times
        self.attempt_times = attempt_times
        self.complete = complete

        # private vars for internal use
        self.__start_time = time.time()
        self.__elapsed_time = time.time()

    def correct(self):
        '''
        Handles case when question answered correctly
        '''

        time_diff = self.time_step()

        self.attempt_times[self.attempts] = time_diff
        self.attempts += 1

        self.total_time = time_diff
        self.correct = True

        self.complete()

    def incorrect(self, last=False):
        '''
        Handles case when question answered incorrectly

        Parameters:
            last: Boolean representing whether or not this is the "last" incorrect allowed
        '''

        time_diff = self.time_step()

        self.attempt_times[self.attempts] = time_diff
        self.attempts += 1

        if (last):
            self.total_time = time_diff
            self.correct = False  # just to make sure

            self.complete()

    def hint(self):
        '''
        Handles case when hint is requested
        '''

        time_diff = self.time_step()

        self.hint_times[self.hints] = time_diff
        self.hints += 1

    def time_step(self):
        '''
        Updates __elapsed_time
        Returns Float representing (ms) difference between __elapsed_time and __start_time
        '''
        self.__elapsed_time = time.time()
        return self.__elapsed_time - self.__start_time

    def complete(self):
        '''
        Called when question is complete to perform cleanup operations
        '''

        while len(self.hint_times) < self.MAX_HINTS:
            self.hint_times.append(-1)

        while len(self.attempt_times) < self.MAX_ATTEMPTS:
            self.hint_times.append(-1)

        self.complete = True

    def __repr__(self):
        return "Question(q_num=%r, attempts=%r, hints=%r, correct=%r, total_time=%r, complete=%r, \\\nhint_times=%s, attempt_times=%s)" % \
            (self.question_num, self.attempts, self.hints, self.correct, self.total_time, self.complete,
             pformat(list(self.hint_times)), pformat(list(self.attempt_times)))
