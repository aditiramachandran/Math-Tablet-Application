# extracts attempt distributions in relation to hint requests across all four sessions and outputs to a csv
# usage: python attempt_distribution_extraction.py <input csv> <output csv>
import os
import sys

def main():
	if len(sys.argv) == 3:
		infile = open(sys.argv[1], 'r')
		outfile = open(sys.argv[2], 'w')
		participant_number = 0

		# initialize arrays to hold sums of attempt distributions
		control_vals = 16 * [0]
		adapt_vals = 16 * [0]

		for line in infile:
			tokens = line.strip().split(",")
			# remove outliers
			if participant_number != 0 and participant_number != 3 and participant_number != 19 and participant_number != 20 and participant_number != 22:
				# sum totals of attempts before hint1, before hint2, before hint3, and after hint3 across four sessions
				for i in range(4):
					if tokens[1] == '0':
					  control_vals[i] += int(tokens[i + 10])
					  control_vals[i + 4] += int(tokens[i + 22])
					  control_vals[i + 8] += int(tokens[i + 34])
					  control_vals[i + 12] += int(tokens[i + 46])
					elif tokens[1] == '1':
					  adapt_vals[i] += int(tokens[i + 10])
					  adapt_vals[i + 4] += int(tokens[i + 22])
					  adapt_vals[i + 8] += int(tokens[i + 34])
					  adapt_vals[i + 12] += int(tokens[i + 46])

			participant_number += 1
		
		# output control values
		outfile.write('Before_hint_1,Before_hint_2,Before_hint_3,After_hint_3\n')
		for i in range(16):
			if (i % 4) - 3 == 0:
				outfile.write(str(control_vals[i]) + '\n')
			else:
				outfile.write(str(control_vals[i]) + ',')
			
		# output adaptive model values
		outfile.write('Before_hint_1,Before_hint_2,Before_hint_3,After_hint_3\n')
		for i in range(16):
			if (i % 4) - 3 == 0:
				outfile.write(str(adapt_vals[i]) + '\n')
			else:
				outfile.write(str(adapt_vals[i]) + ',')
			
	else:
		print 'usage: python attempt_distribution_extraction.py <input csv> <output csv>'

if __name__ == "__main__": 
	main()
