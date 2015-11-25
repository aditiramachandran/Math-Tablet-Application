# this script joins excel columns together into a new output csv
# usage: python splicer.py <output csv> [<input csv> <[column number(s)]>]*

import os
import sys

def main():
  if len(sys.argv) >= 4:
    infile = open(sys.argv[2], 'r')
    data = infile.readlines()
    data = [''] * len(data)

    index = 2
    while index < len(sys.argv):
      infile = open(sys.argv[index], 'r')
      cols = sys.argv[index + 1]
      cols = cols[1:-1]
      colnums = cols.split(',')
      colnums = map(int, colnums)

      info = infile.readlines()
      for i in range(len(data)):
        tokens = info[i].strip().split(",")
        for j in colnums:
          data[i] += str(tokens[j]) + ','

      index += 2

    outfile = open(sys.argv[1], 'w')
    outfile.writelines([x + '\n' for x in data])
  else:
    print "usage: python compare_features.py <output csv> [<input csv> <column number>]*"

if __name__ == "__main__": 
  main()
