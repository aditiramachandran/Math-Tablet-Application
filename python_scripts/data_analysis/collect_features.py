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
    num_before_hint1 = 0
    num_before_hint2 = 0
    num_before_hint3 = 0
    num_after_hint3 = 0
    incorrect_flag = False
    hint1_flag = False
    hint2_flag = False
    hint3_flag = False
    attempt_flag = False
    denied_flag = False
    consec_attempts = 0
    problem_starttime = 0
    time_until_hint1 = 0
    num_without_hint = 0
    time_normalized_sum = 0

    for line in session:
      tokens = line.strip().split(",")

      # checks for a robot restart w/ time delay
      restart_flag = False
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
          incorrect_flag = False
          hint1_flag = False
          hint2_flag = False
          hint3_flag = False
          attempt_flag = False
          restart_flag = False
          consec_attempts = 0

          if problem_starttime == 0:
            problem_starttime = current_timestamp
          else:
            if not restart_flag and time_until_hint1 != 0:
              problem_length = current_timestamp - problem_starttime
              time_normalized = time_until_hint1 / problem_length.total_seconds()
              time_normalized_sum += time_normalized
              print 'time until hint1 is ' + str(time_until_hint1)
              print 'time for problem is ' + str(problem_length.total_seconds())
            problem_starttime = current_timestamp
            time_until_hint1 = 0

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
              num_without_hint += 1
          elif not hint1_flag and not hint2_flag and not hint3_flag:
            num_without_hint += 1
        elif current_type == 'HINT 1':
          consec_attempts = 0
          if not hint1_flag:
            hint1_flag = True
            num_hints_requested += 1
            num_problems_hint_received += 1
            attempt_flag = False
            if tokens[self.OTHER_INFO] == 'automatic':
              num_auto_hints += 1
            time_until_hint1 = current_timestamp - problem_starttime
            time_until_hint1 = time_until_hint1.total_seconds()
        elif current_type == 'HINT 2':
          consec_attempts = 0
          if not hint2_flag:
            hint2_flag = True
            num_hints_requested += 1
            if tokens[self.OTHER_INFO] == 'automatic':
              num_auto_hints += 1
        elif current_type == 'HINT 3':
          consec_attempts = 0
          if not hint3_flag:
            hint3_flag = True
            num_hints_requested += 1
            if not attempt_flag:
              num_denied_hints += 1
            if tokens[self.OTHER_INFO].strip() == 'automatic':
              num_auto_hints += 1
        elif current_type == 'DENIED HINT':
          if not denied_flag:
            num_denied_hints += 1
          denied_flag = True
        elif current_type == 'END':
          if not restart_flag and time_until_hint1 != 0:
            problem_length = current_timestamp - problem_starttime
            time_normalized = time_until_hint1 / problem_length.total_seconds()
            time_normalized_sum += time_normalized
          problem_starttime = 0
          time_until_hint1 = 0

        # resets the flag so that we don't discount a legitimate double denial of hint
        if current_type == 'QUESTION' or current_type == 'INCORRECT' or current_type == 'HINT 1' or current_type == 'HINT 2' or current_type == 'HINT 3':
          denied_flag = False

        if current_type == 'CORRECT' or current_type == 'INCORRECT' or current_type == 'LAST INCORRECT':
          if hint3_flag:
            num_after_hint3 += 1
          elif hint2_flag:
            num_before_hint3 += 1
          elif hint1_flag:
            num_before_hint2 += 1
          else:
            num_before_hint1 += 1

    time_normalized_average = 0
    if num_without_hint < self.num_questions_per_session:
      time_normalized_average = time_normalized_sum / (self.num_questions_per_session - num_without_hint)

    #print "pid", pid, ": ", num_incorrects, ", ", num_corrects, ", ", num_corrects_first_try, ", ", num_corrects_first_try_no_hints, ", ", num_hints_requested, ", ", num_problems_hint_received
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
    self.feature_structure[pid][session_num]["average_time_until_hint1_normalized"] = time_normalized_average
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
      out.write(",average_time_until_hint1_normalized_S"+str(i))
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
        out.write(","+str(self.feature_structure[participant][i]["average_time_until_hint1_normalized"]))
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
