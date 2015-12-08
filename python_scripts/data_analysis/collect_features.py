import os
import sys
import re
import fnmatch
import collections
from datetime import datetime

class Analysis:
  def __init__(self, inputDir, outputFile):
    self.inputDir = inputDir
    self.outputFile = outputFile
    self.TOTAL_NUM_SESSIONS = 4
    self.PID = 0
    self.GROUP = 1
    self.SESSION_NUM = 2
    self.TIMESTAMP = 3
    self.QUESTION_NUM = 4
    self.TYPE = 5
    self.OTHER_INFO = 6
    self.num_questions_per_session = 8
    self.feature_structure = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    self.groups = {}
  
  def parse_directory(self):
    #directory = open(self.inputDir)
    for root, dirs, files in os.walk(self.inputDir):
      #for dir in dirs:
        #print os.path.join(root, dir)
      for filename in files:
        #print filename
        if fnmatch.fnmatch(filename, 'P*_S?.txt'):
          filename = os.path.join(root, filename)
          #print filename
          self.collect_basic_features(filename)


  def collect_basic_features(self,indivFile):
    session = open(indivFile)
    pid = 0
    session_num = 0
    exp_group = -1

    num_problems_hint_received = 0
    num_hints_requested = 0
    num_incorrects = 0
    num_corrects = 0
    num_corrects_first_try = 0
    num_corrects_first_try_no_hints = 0
    potential_auto_hints = 0 #would be triggered if in adaptive
    num_denied_hints = 0 #actually triggered for adaptive group
    num_auto_hints = 0 #actually triggered for adaptive group
    num_late_hints = 0 # number of hints 2 and 3
    num_late_hints_no_restart = 0
    num_late_attempts = 0 # number of attempts between hints 1&2 and hints 2&3
    num_before_hint1 = 0
    num_before_hint2 = 0
    num_before_hint3 = 0
    num_after_hint3 = 0
    num_erratic_hint_requests = 0
    num_before_hint1_temp = 0 # per problem, used to subtract out non hint questions
    incorrect_flag = False
    hint1_flag = False
    hint2_flag = False
    hint3_flag = False
    attempt_flag = False
    denied_flag = False
    restart_flag = False
    restarted_on_question = False
    num_hints_until_correct = 0
    consec_attempts = 0
    problem_starttime = 0
    num_restarts_with_hint = 0
    time_until_hint1 = 0
    time_normalized_sum_hint1 = 0
    last_speech_timestamp = 0
    last_hint_timestamp = 0
    total_problem_length = 0
    current_attempts_between_hints = 0 # reset every time a hint is requested
    total_time_between_late_hints = 0
    intermediate_time_between_late_hints = 0

    for line in session:
      tokens = line.strip().split(",")

      # checks for a robot restart w/ time delay
      try:
        if tokens[len(tokens) - 1] == 'RESTART':
          restart_flag = True
      except:
        pass

      if len(tokens) > 5:
        # extracts timestamp for event
        current_timestamp = tokens[self.TIMESTAMP]
        if current_timestamp != 'TIMESTAMP':
          fmt = '%Y-%m-%d %H:%M:%S.%f'
          current_timestamp = datetime.strptime(current_timestamp, fmt)

        current_type = tokens[self.TYPE]
        if current_type == 'START':
          pid = int(tokens[self.PID])
          session_num = int(tokens[self.SESSION_NUM])
          if session_num == self.TOTAL_NUM_SESSIONS: #if they made it through all 4 sessions
            exp_group = int(tokens[self.GROUP])
            self.groups[pid] = exp_group
        elif current_type == 'QUESTION':
          problem_starttime = current_timestamp
        elif current_type == 'INCORRECT':
          incorrect_flag = True
          num_incorrects += 1
          consec_attempts += 1
          if hint1_flag:
            attempt_flag = True
          if not hint3_flag and consec_attempts==2: #if hint 3 hasnt been triggered, there's an auto hint to give
            potential_auto_hints += 1
            consec_attempts = 0
        elif current_type == 'LAST INCORRECT':
          num_incorrects += 1
        elif current_type == 'CORRECT':
          num_corrects += 1
          if not incorrect_flag:
            num_corrects_first_try += 1
            if not hint1_flag and not hint2_flag and not hint3_flag:
              num_corrects_first_try_no_hints += 1
        elif current_type == 'HINT 1':
          if not hint1_flag:
            hint1_flag = True
            num_hints_requested += 1
            num_problems_hint_received += 1
            attempt_flag = False
            if tokens[self.OTHER_INFO] == 'automatic':
              num_auto_hints += 1
            time_until_hint1 = current_timestamp - problem_starttime
            time_until_hint1 = time_until_hint1.total_seconds()
          else:
            num_erratic_hint_requests += 1
        elif current_type == 'HINT 2':
          if not hint2_flag:
            hint2_flag = True
            num_hints_requested += 1
            num_late_hints += 1
            if not restart_flag:
              num_late_hints_no_restart += 1
            if tokens[self.OTHER_INFO] == 'automatic':
              num_auto_hints += 1
            time_between_hints = current_timestamp - last_hint_timestamp
            intermediate_time_between_late_hints += time_between_hints.total_seconds()
          else:
            num_erratic_hint_requests += 1
        elif current_type == 'HINT 3':
          if not hint3_flag:
            hint3_flag = True
            num_hints_requested += 1
            num_late_hints += 1
            if not restart_flag:
              num_late_hints_no_restart += 1
            if not attempt_flag:
              num_denied_hints += 1
            if tokens[self.OTHER_INFO].strip() == 'automatic':
              num_auto_hints += 1
            time_between_hints = current_timestamp - last_hint_timestamp
            intermediate_time_between_late_hints += time_between_hints.total_seconds()
          else:
            num_erratic_hint_requests += 1
        elif current_type == 'DENIED HINT':
          if not denied_flag:
            num_denied_hints += 1
          denied_flag = True
        elif current_type == 'ROBOT SPEECH':
          last_speech_timestamp = current_timestamp

        # resets the flag so that we don't discount a legitimate double denial of hint
        if current_type == 'QUESTION' or current_type == 'INCORRECT' or current_type == 'HINT 1' or current_type == 'HINT 2' or current_type == 'HINT 3':
          denied_flag = False

        if current_type == 'HINT 1' or current_type == 'HINT 2' or current_type == 'HINT 3':
          consec_attempts = 0
          current_attempts_between_hints = 0
          last_hint_timestamp = current_timestamp

        if current_type == 'CORRECT' or current_type == 'INCORRECT' or current_type == 'LAST INCORRECT':
          current_attempts_between_hints += 1
          if hint3_flag:
            num_after_hint3 += 1
          elif hint2_flag:
            num_before_hint3 += 1
            num_late_attempts += 1
          elif hint1_flag:
            num_before_hint2 += 1
            num_late_attempts += 1
          else:
            num_before_hint1 += 1
            num_before_hint1_temp += 1
        
        if current_type == 'CORRECT':
          if hint1_flag:
            num_hints_until_correct += 1
          if hint2_flag:
            num_hints_until_correct += 1
          if hint3_flag:
            num_hints_until_correct += 1

        # reset everything
        if current_type == 'CORRECT' or current_type == 'LAST INCORRECT':
          if not hint1_flag:
            num_before_hint1 -= num_before_hint1_temp
          elif restart_flag:
            num_restarts_with_hint += 1

          # calculating attempts strictly sandwiched between hints
          if hint3_flag:
            pass
          elif hint2_flag or hint1_flag:
            num_late_attempts -= current_attempts_between_hints
          current_attempts_between_hints = 0

          incorrect_flag = False
          hint1_flag = False
          hint2_flag = False
          hint3_flag = False
          attempt_flag = False
          consec_attempts = 0
          num_before_hint1_temp = 0

          problem_length = last_speech_timestamp - problem_starttime
          total_problem_length += problem_length.total_seconds()
          if not restart_flag and time_until_hint1 != 0:
            time_normalized_hint1 = time_until_hint1 / problem_length.total_seconds()
            time_normalized_sum_hint1 += time_normalized_hint1
            time_normalized_late = intermediate_time_between_late_hints / problem_length.total_seconds()
            total_time_between_late_hints += time_normalized_late
          intermediate_time_between_late_hints = 0
          time_until_hint1 = 0

          restart_flag = False


    time_normalized_average_hint1 = 0
    if num_problems_hint_received - num_restarts_with_hint > 0:
      time_normalized_average_hint1 = time_normalized_sum_hint1 / (num_problems_hint_received - num_restarts_with_hint)

    average_attempts_before_hint1 = 0
    if num_problems_hint_received > 0:
      average_attempts_before_hint1 = float(num_before_hint1) / float(num_problems_hint_received)

    average_attempts_between_hints = 0
    if num_late_hints > 0:
      average_attempts_between_hints = float(num_late_attempts) / float(num_late_hints)

    average_time_between_hints = 0
    if num_late_hints_no_restart > 0:
      average_time_between_hints = total_time_between_late_hints / float(num_late_hints_no_restart)

    average_num_hints_until_correct = 0
    if num_corrects > 0:
      average_num_hints_until_correct = num_hints_until_correct / float(num_corrects)

    print "pid,session:", pid, ",", session_num, " --> ", potential_auto_hints, ", ", num_auto_hints
    self.feature_structure[pid][session_num]["num_incorrects"] = num_incorrects
    self.feature_structure[pid][session_num]["num_corrects"] = num_corrects
    self.feature_structure[pid][session_num]["num_corrects_first_try"] = num_corrects_first_try
    self.feature_structure[pid][session_num]["num_corrects_first_try_no_hints"] = num_corrects_first_try_no_hints
    self.feature_structure[pid][session_num]["num_hints_requested"] = num_hints_requested
    self.feature_structure[pid][session_num]["num_problems_hint_received"] = num_problems_hint_received
    self.feature_structure[pid][session_num]["num_denied_hints"] = num_denied_hints
    self.feature_structure[pid][session_num]["potential_auto_hints"] = potential_auto_hints
    self.feature_structure[pid][session_num]["num_before_hint1"] = num_before_hint1
    self.feature_structure[pid][session_num]["num_before_hint2"] = num_before_hint2
    self.feature_structure[pid][session_num]["num_before_hint3"] = num_before_hint3
    self.feature_structure[pid][session_num]["num_after_hint3"] = num_after_hint3
    self.feature_structure[pid][session_num]["num_erratic_hint_requests"] = num_erratic_hint_requests
    self.feature_structure[pid][session_num]["average_attempts_before_hint1"] = average_attempts_before_hint1
    self.feature_structure[pid][session_num]["average_time_until_hint1_normalized"] = time_normalized_average_hint1
    self.feature_structure[pid][session_num]["average_problem_length"] = total_problem_length / self.num_questions_per_session
    self.feature_structure[pid][session_num]["average_attempts_between_hints"] = average_attempts_between_hints
    self.feature_structure[pid][session_num]["average_time_between_hints_normalized"] = average_time_between_hints
    self.feature_structure[pid][session_num]["average_num_hints_until_correct"] = average_num_hints_until_correct
    session.close()   


  
  def write_output(self):
    #iterate through data structure and write to self.outputFile
    out = open(self.outputFile, 'w')
    out.write("PID,GROUP")
    for i in range(1,self.TOTAL_NUM_SESSIONS+1):
      out.write(",num_incorrects_S"+str(i))
      out.write(",num_corrects_S"+str(i))
      out.write(",num_corrects_first_try_S"+str(i))
      out.write(",num_corrects_first_try_no_hint_S"+str(i))
      out.write(",num_hints_requested_S"+str(i))
      out.write(",num_problems_hint_received_S"+str(i))
      out.write(",num_denied_hints_S"+str(i))
      out.write(",potential_auto_hints_S"+str(i))
      out.write(",num_attempts_before_hint1_S"+str(i))
      out.write(",num_attempts_before_hint2_S"+str(i))
      out.write(",num_attempts_before_hint3_S"+str(i))
      out.write(",num_attempts_after_hint3_S"+str(i))
      out.write(",num_erratic_hint_requests_S"+str(i))
      out.write(",average_attempts_before_hint1_S"+str(i))
      out.write(",average_time_until_hint1_normalized_S"+str(i))
      out.write(",average_problem_length_S"+str(i))
      out.write(",average_attempts_between_hints_S"+str(i))
      out.write(",average_time_between_hints_normalized_S"+str(i))
      out.write(",average_num_hints_until_correct_S"+str(i))
    out.write("\n") 
    #print self.feature_structure
    for participant in self.feature_structure.keys():
      exp_group = -1
      if participant in self.groups.keys():
        exp_group = self.groups[participant]
      out.write(str(participant)+","+str(exp_group))
      for i in range(1,self.TOTAL_NUM_SESSIONS+1):
        out.write(","+str(self.feature_structure[participant][i]["num_incorrects"]))
        out.write(","+str(self.feature_structure[participant][i]["num_corrects"]))
        out.write(","+str(self.feature_structure[participant][i]["num_corrects_first_try"]))
        out.write(","+str(self.feature_structure[participant][i]["num_corrects_first_try_no_hints"]))
        out.write(","+str(self.feature_structure[participant][i]["num_hints_requested"]))
        out.write(","+str(self.feature_structure[participant][i]["num_problems_hint_received"]))
        out.write(","+str(self.feature_structure[participant][i]["num_denied_hints"]))
        out.write(","+str(self.feature_structure[participant][i]["potential_auto_hints"]))
        out.write(","+str(self.feature_structure[participant][i]["num_before_hint1"]))
        out.write(","+str(self.feature_structure[participant][i]["num_before_hint2"]))
        out.write(","+str(self.feature_structure[participant][i]["num_before_hint3"]))
        out.write(","+str(self.feature_structure[participant][i]["num_after_hint3"]))
        out.write(","+str(self.feature_structure[participant][i]["num_erratic_hint_requests"]))
        out.write(","+str(self.feature_structure[participant][i]["average_attempts_before_hint1"]))
        out.write(","+str(self.feature_structure[participant][i]["average_time_until_hint1_normalized"]))
        out.write(","+str(self.feature_structure[participant][i]["average_problem_length"]))
        out.write(","+str(self.feature_structure[participant][i]["average_attempts_between_hints"]))
        out.write(","+str(self.feature_structure[participant][i]["average_time_between_hints_normalized"]))
        out.write(","+str(self.feature_structure[participant][i]["average_num_hints_until_correct"]))
      out.write("\n")
    out.close()     


def main():
  if len(sys.argv) == 3:
    #print 'input dir is: ', sys.argv[1]
    #print 'output file is: ', sys.argv[2]
    analysis = Analysis(sys.argv[1], sys.argv[2])
    analysis.parse_directory()
    analysis.write_output()
  else:
    print 'usage: python collect_features.py <input dir> <output file>'


if __name__ == "__main__": 
  main()
