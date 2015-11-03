# extracts denied hints and auto hints from collect_features.py and outputs to a csv
# flag 1 denotes that we extract only session 1 data rather than all sessions
# flag 2 denotes that we separate data by session and group (control or adapt)
# usage: python denied_auto_hints_extraction.py <input csv> <output csv> <optional flag>
import os
import sys

def main():
	if len(sys.argv) == 3 or len(sys.argv) == 4:
		infile = open(sys.argv[1], 'r')
		outfile = open(sys.argv[2], 'w')

		session1_flag = 0
		try:
			session1_flag = int(sys.argv[3])
		except:
			pass

		# contains sum totals of denied hints across 4 sessions, then sum totals of auto hints
		control_vals = 8 * [0] 
		adapt_vals = 8 * [0]

		participant_number = 0
		for line in infile:
			tokens = line.strip().split(",")
			if participant_number == 0:
				# comment in if label needed
			  # outfile.write('Denied Hints,Auto Hints\n')
				pass
			# remove bad participants
			elif participant_number != 3 and participant_number != 19 and participant_number != 20 and participant_number != 22:
				# write only session 1 denied/auto hints
				if session1_flag == 1:
					outfile.write(tokens[8] + ',' + tokens[9] + '\n')
				# sum totals of denied/auto hints distributed across session and group
				elif session1_flag == 2:
					for i in range(2):	
					  if tokens[1] == '0':
					    control_vals[i * 4] += int(tokens[i + 8])
					    control_vals[i * 4 + 1] += int(tokens[i + 20])
					    control_vals[i * 4 + 2] += int(tokens[i + 32])
					    control_vals[i * 4 + 3] += int(tokens[i + 44])
					  elif tokens[1] == '1':
					    adapt_vals[i * 4] += int(tokens[i + 8])
					    adapt_vals[i * 4 + 1] += int(tokens[i + 20])
					    adapt_vals[i * 4 + 2] += int(tokens[i + 32])
					    adapt_vals[i * 4 + 3] += int(tokens[i + 44])
	
	      # find total denied/auto hints and writes
				else:
				  total_denied_hints = int(tokens[8]) + int(tokens[20]) + int(tokens[32]) + int(tokens[44])
				  total_auto_hints = int(tokens[9]) + int(tokens[21]) + int(tokens[33]) + int(tokens[45])
				  outfile.write(str(total_denied_hints) + ',' + str(total_auto_hints) + '\n')
				
			participant_number += 1
		
		if session1_flag == 2:
			for i in range(8):
			  outfile.write(str(control_vals[i]) + ',')
			outfile.write('\n')

			for i in range(8):
				outfile.write(str(adapt_vals[i]) + ',')
			outfile.write('\n')

	else:
		print 'usage: denied_auto_hints_extraction.py <input csv> <output file> <optional flag>'

if __name__ == "__main__": 
	main()
