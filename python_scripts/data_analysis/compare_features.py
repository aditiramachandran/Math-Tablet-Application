# compares two features using a very specific set of flags
# designed to take in the output of collect_features.py
# flag 1 denotes that we extract only session 1 data rather than all sessions (0 for session1, 1 for session1 including participant3, 2 for all sessions)
# flag 2 denotes that we take the aggregate of a column rather than each individual column - 0 for individual consideration, 1 for sum, and 2 for average
# flag 3 denotes that we separate data by session and group (0 for nothing, 1 for separation of control/adapt (for two separate graphs))
# colnums denotes which columns to use - a comma separated array of column numbers used
# usage: python compare_features.py <input csv> <output csv> <flag 1> <flag 2> <flag 3> <[colnums]>
import os
import sys

NUM_SESSIONS = 4

def main():
  if len(sys.argv) == 7:
    infile = open(sys.argv[1], 'r')
    outfile = open(sys.argv[2], 'w')
    temp_file = open('tempfile99', 'w')

    num_participants = 29
    num_control_participants = 14
    num_adapt_participants = 15
    session_flag = 0
    aggregate_flag = 0
    control_flag = 0
    colnums = []
    try:
      session_flag = int(sys.argv[3])
      aggregate_flag = int(sys.argv[4])
      control_flag = int(sys.argv[5])
      cols = sys.argv[6]
      cols = cols[1:-1]
      colnums = cols.split(',')
      colnums = map(int, colnums)
    except:
      pass

    num_cols = len(colnums)
    num_cols_total = num_cols
    if session_flag == 2:
      num_cols_total *= NUM_SESSIONS
    elif session_flag == 1: # add one to participants if we include #3
      num_participants += 1

    # constructing an array of column numbers across sessions
    interval_len = (len(infile.readline().strip().split(",")) - 2) / NUM_SESSIONS
    if session_flag == 2:
      for i in range(num_cols_total - num_cols):
        colnums.append(colnums[len(colnums) - num_cols] + interval_len)

    # contains sum totals of values across 4 sessions
    # only used if aggregate_flag == 0 or aggregate_flag == 1
    control_vals = num_cols_total * [0] 
    adapt_vals = num_cols_total * [0]

    participant_number = 1
    for line in infile:
      tokens = line.strip().split(",")
      # remove bad participants
      if participant_number != 19 and participant_number != 20 and participant_number != 22 and (participant_number != 3 or session_flag == 1):
        if control_flag == 0:
          # outputting each individual row
          if aggregate_flag == 0:
            # writes column values in order specified
            for i in range(num_cols_total):
              outfile.write(tokens[colnums[i]] + ',')
            outfile.write('\n')
          # taking the aggregate of each row
          elif aggregate_flag == 1 or aggregate_flag == 2:
            for i in range(num_cols_total):
              control_vals[i] += float(tokens[colnums[i]])
        elif control_flag == 1: # separate out into adapt/control group
          if aggregate_flag == 0:
            if tokens[1] == '0': # control group
              for i in range(num_cols):
                outfile.write(tokens[colnums[i]] + ',')
              outfile.write('\n')
            elif tokens[1] == '1': # adapt group
              for i in range(num_cols):
                temp_file.write(tokens[colnums[i]] + ',')
              temp_file.write('\n')
          elif aggregate_flag == 1 or aggregate_flag == 2: # add up control_vals and adapt_vals
            if tokens[1] == '0':
              for i in range(num_cols_total):
                control_vals[i] += float(tokens[colnums[i]])
            elif tokens[1] == '1':
              for i in range(num_cols_total):
                adapt_vals[i] += float(tokens[colnums[i]])
                    
      participant_number += 1


    if control_flag == 1 and aggregate_flag == 0:
      temp_file = open('tempfile99', 'r')
      outfile.write('\n')
      for t in temp_file:
        outfile.write(t)
      os.remove('tempfile99')
    elif aggregate_flag == 1 or aggregate_flag == 2:
      # outfile.write('note: ordered by session number going down\n');
      for i in range(num_cols_total):
        if aggregate_flag == 1:
          outfile.write(str(control_vals[i]) + ',')
        elif aggregate_flag == 2:
          if control_flag == 1:
            outfile.write(str(control_vals[i] / float(num_control_participants)) + ',')
          else:
            outfile.write(str(control_vals[i] / float(num_participants)) + ',')

        if (i + 1) % num_cols == 0:
          outfile.write('\n')

      if control_flag == 1:
        outfile.write('\n')
        for i in range(num_cols_total):
          if aggregate_flag == 1:
            outfile.write(str(adapt_vals[i]) + ',')
          elif aggregate_flag == 2:
            outfile.write(str(adapt_vals[i] / float(num_adapt_participants)) + ',')

          if (i + 1) % num_cols == 0:
            outfile.write('\n')

  else:
    print 'usage: python compare_features.py <input csv> <output csv> <flag 1> <flag 2> <flag 3> <[colnums]>'

if __name__ == "__main__": 
  main()
