# extracts denied hints and auto hints from collect_features.py and outputs to a csv
# usage: python denied_auto_hints_extraction.py <input csv> <output csv>
import os
import sys

def main():
	if len(sys.argv) == 3:
		infile = open(sys.argv[1], 'r')
		outfile = open(sys.argv[2], 'w')
		participant_number = 0
		for line in infile:
			tokens = line.strip().split(",")
			if participant_number == 0:
				# comment in if label needed
			  # outfile.write('Denied Hints,Auto Hints\n')
				pass
			# remove bad participants
			elif participant_number != 3 and participant_number != 19 and participant_number != 20 and participant_number != 22:
				# find total denied/auto hints and writes
				total_denied_hints = int(tokens[8]) + int(tokens[20]) + int(tokens[32]) + int(tokens[44])
				total_auto_hints = int(tokens[9]) + int(tokens[21]) + int(tokens[33]) + int(tokens[45])
				outfile.write(str(total_denied_hints) + ',' + str(total_auto_hints) + '\n')
				
			participant_number += 1
	else:
		print 'usage: denied_auto_hints_extraction.py <input csv> <output file>'

if __name__ == "__main__": 
	main()
