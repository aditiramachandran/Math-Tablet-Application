# given an input file, normalize all the columns to a range of 0 to 1
# usage: python normalize.py <input csv> <output csv>

import os
import sys

def normalize(val, mincol, maxcol):
  return (val - mincol) / (maxcol - mincol)

def main():
  if len(sys.argv) == 3:
    infile = open(sys.argv[1], 'r')
    inmat = infile.readlines()
    tokens = inmat[0].strip().split(",")
    datamat = [] 
    for i in range(len(tokens)):
      datamat.append([])
    dataoutput = [''] * len(inmat)

    for i in range(len(inmat)):
      tokens = inmat[i].strip().split(",")
      for j in range(len(tokens)):
        datamat[j].append(float(tokens[j]))

    for i in range(len(datamat)):
      col = datamat[i]
      for j in range(len(col)):
        dataoutput[j] += str(normalize(col[j], min(col), max(col))) + ','

    outfile = open(sys.argv[2], 'w')
    outfile.writelines([x[:-1] + '\n' for x in dataoutput])

  else:
    print 'usage: python compare_features.py <input csv> <output csv> <flag 1> <flag 2> <flag 3> <[colnums]>'

if __name__ == "__main__": 
  main()
