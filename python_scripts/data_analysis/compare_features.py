# compares two features using a very specific set of flags
# designed to take in the output of collect_features.py
# flag 1 denotes that we extract only session 1 data rather than all sessions (0 for session1, 1 for session1 including participant3, 2 for all sessions)
# flag 2 denotes that we take the aggregate of a column rather than each individual column - 0 for sum, 1 for average, and 2 for individual consideration
# flag 3 denotes that we separate data by session and group (0 for nothing, 1 for separation of control/adapt (for two separate graphs))
# flag 4 denotes how many separate data points to choose from (usually 2, sometimes 3)
# colnums denotes which columns to use - a comma separated array of column numbers used
# usage: python compare_features.py <input csv> <output csv> <flag 1> <flag 2> <flag 3> <flag 4> <[colnums]>
import os
import sys

NUM_SESSIONS = 4

def main():
  if len(sys.argv) == 8:
    infile = open(sys.argv[1], 'r')
    outfile = open(sys.argv[2], 'w')

    session_flag = 0
    aggregate_flag = 0
    control_flag = 0
    col3_flag = 0
    colnums = []
    try:
      session_flag = int(sys.argv[3])
      aggregate_flag = int(sys.argv[4])
      control_flag = int(sys.argv[5])
      num_compares = int(sys.argv[6])
      cols = sys.argv[7]
      cols = cols[1:-1]
      colnums = cols.split(',')
      colnums = map(int, colnums)
    except:
      pass

    # continue checking for proper inputs
    num_cols = len(colnums)
    if session_flag == 0 or session_flag == 1:
      assert num_cols == num_compares
    elif session_flag == 2 or session_flag == 3:
      assert num_cols == num_compares * NUM_SESSIONS

    # contains sum totals of values across 4 sessions
    # only used if aggregate_flag == 1 or aggregate_flag == 2
    control_vals = num_cols * [0] 
    adapt_vals = num_cols * [0]
    aggregate_vals = num_cols * [0]

    participant_number = 0
    for line in infile:
      tokens = line.strip().split(",")
      if participant_number == 0:
        # print here if label needed
        pass
      # remove bad participants
      elif participant_number != 19 and participant_number != 20 and participant_number != 22 and (participant_number != 3 or session_flag == 1):
        # taking the aggregate of each row
        if aggregate_flag == 0 or aggregate_flag == 1:
          pass
        # outputting each individual row
        elif aggregate_flag == 2:
          if control_flag == 0:
            # write only session 1 columns
            if session_flag == 0 or session_flag == 1:
              for i in range(num_compares):
                outfile.write(tokens[colnums[i]] + ',')
              outfile.write('\n')
            # analysis for all 4 sessions
            #elif session_flag == 2:
               
          # find total denied/auto hints and writes
          #else:
          #  total_denied_hints = int(tokens[8]) + int(tokens[20]) + int(tokens[32]) + int(tokens[44])
          #  total_auto_hints = int(tokens[9]) + int(tokens[21]) + int(tokens[33]) + int(tokens[45])
          #  outfile.write(str(total_denied_hints) + ',' + str(total_auto_hints) + '\n')
       
      participant_number += 1
    
          #for i in range(2):
          #  if tokens[1] == '0':
          #    control_vals[i * 4] += int(tokens[i + 8])
          #    control_vals[i * 4 + 1] += int(tokens[i + 20])
          #    control_vals[i * 4 + 2] += int(tokens[i + 32])
          #    control_vals[i * 4 + 3] += int(tokens[i + 44])
          #  elif tokens[1] == '1':
          #    adapt_vals[i * 4] += int(tokens[i + 8])
          #    adapt_vals[i * 4 + 1] += int(tokens[i + 20])
          #    adapt_vals[i * 4 + 2] += int(tokens[i + 32])
          #    adapt_vals[i * 4 + 3] += int(tokens[i + 44])

    #if session1_flag == 2:
    #  for i in range(8):
    #    outfile.write(str(control_vals[i]) + ',')
    #  outfile.write('\n')

    #  for i in range(8):
    #    outfile.write(str(adapt_vals[i]) + ',')
    #  outfile.write('\n')

  else:
    print 'usage: python compare_features.py <input csv> <output csv> <flag 1> <flag 2> <flag 3> <[colnums]>'

if __name__ == "__main__": 
  main()
