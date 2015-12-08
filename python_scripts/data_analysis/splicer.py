# this script joins excel columns together into a new output csv
# flag 1 indicates truncation of first line - 0 to maintain, 1 to truncate
# flag 2 - 0 for deletion of participants 3, 19, 20, 22, 1 to retain participant 3, and 2 to retain all 4
# usage: python splicer.py <flag 1> <flag 2> <output csv> [<input csv> <[column number(s)]>]*

import os
import sys

def main():
  if len(sys.argv) >= 6:
    truncate_flag = int(sys.argv[1])
    assert truncate_flag == 0 or truncate_flag == 1
    deletion_flag = int(sys.argv[2])
    assert deletion_flag >= 0 and deletion_flag <= 2

    subtract = truncate_flag
    if deletion_flag == 0:
      subtract += 4
    elif deletion_flag == 1:
      subtract += 3

    infile = open(sys.argv[4], 'r')
    data = infile.readlines()
    data = [''] * (len(data) - subtract)

    index = 4
    while index < len(sys.argv):
      infile = open(sys.argv[index], 'r')
      cols = sys.argv[index + 1]
      cols = cols[1:-1]
      colnums = cols.split(',')
      colnums = map(int, colnums)

      info = infile.readlines()
      dindex = 0
      for i in range(truncate_flag, len(info)):
        if ((deletion_flag == 2) or (i != 19 and i != 20 and i != 22 and (i != 3 or deletion_flag == 1))):
          tokens = info[i].strip().split(",")
          for j in colnums:
            if j == 19:
              data[dindex] += str(float(tokens[j]) * 10) + ','
            else:
              data[dindex] += str(tokens[j]) + ','
          dindex += 1

      index += 2

    outfile = open(sys.argv[3], 'w')
    outfile.writelines([x[:-1] + '\n' for x in data])
  else:
    print "usage: python compare_features.py <output csv> [<input csv> <column number>]*"

if __name__ == "__main__": 
  main()
