#!usr/bin/python
# -*- coding: utf-8 -*-

## 	BANK OCR KATA
## 	Josh (Botmasher) playing thru stories found here:
## 	https://github.com/testdouble/contributing-tests/wiki/Bank-OCR-kata
##  Going with first hunches and staying under a few hours => I made spaghetti :D

import re
import math

# Naïve: Hash of seven-segment representation of digits 0-9
# Upgrade: compare seven-segment to alphanum, probability of character match, offer guess
segs = [ '   ' , ' _ ' , '  |' , '|_ ' , ' _|' , '| |' , '|_|' ]
seven_segments = [ \
	[1,5,6], \
	[0,2,2], \
	[1,4,3], \
	[1,4,4], \
	[0,6,2], \
	[1,3,4], \
	[1,3,6], \
	[1,2,2], \
	[1,6,6], \
	[1,6,4], \
]

#for a in seven_segments:
#	print (segs[a[0]]+'\n'+segs[a[1]]+'\n'+segs[a[2]])

#segments_map = {n: seven_segments[n] for n in range(0,len(seven_segments))}

# turn any nested array of triple ints into seven segs
def translate_to_segs (lines):
	segments = [] 
	for l in lines:
		for a in l:
			segments.append([ segs[a[0]],segs[a[1]],segs[a[2]]])
	return segments
	# also do layout, which means rotating/cutting each three

# # not yet implemented; not used below
# def translate_to_indices_array (segs_a):
# 	return None

# # not yet tested; not used below
# def translate_to_indices (a):
# 	if a in seven_segments:
# 		return seven_segments.index(a)
# 	else:
# 		return None

# # turn single seven segments array into an integer
# # superseded by the new off_by_one check
# def translate_seven_segments (a):
# 	# find indices of seg pattern then numeral corresponding to pattern
# 	check_segs_offbyone(a)
# 	try:
# 		seg_indices = [ segs.index(a[0]),segs.index(a[1]),segs.index(a[2]) ]
# 		num = seven_segments.index(seg_indices)
# 		return str(num)
# 	# the segment pattern did not match a numeral
# 	except:
# 		return '?'

# check for well-formed account numbers
def checksum (acct_num, status_code):
	sum_val = sum( int(acct_num[i])*i for i in range(len(acct_num)) )
	if sum_val%11 == 0:
		return status_code
	return ' ERR'

# turn nested line arrays of triple segments into account number digits
# built around seven segs off-by-one function
def translate_line_to_digits (line):
	print_digits = ''
	status = ''
	illegible_wildcard = '?'
	ambiguous_options_lists = []

	# each subarray contains 3 segment sections to be read as one numeral
	for i in range(len(line)):

		segment_array = line[i]

		# find how many numbers this array can represent
		options = check_segs_offbyone(segment_array)

		## Build account number string from options

		# unambiguous or ambiguous and represents a number
		if len(options) >= 1:
			this_digit = str(seven_segments.index(options[0]))
		# unambiguous and does not represent a number
		else:
			status = ' ILL'
			this_digit = illegible_wildcard

		# add this number to final account number and to ambiguous options (if any)
		for amblist in ambiguous_options_lists:
			amblist.append(this_digit)
		print_digits += this_digit

		# 'ambiguous' status (does not override 'illegible' status)
		if len(options) > 1 and illegible_wildcard not in print_digits:
			status = ' AMB'
		
		# iterate through and store the options
		for o_i in range(0,len(options-1)):
			# if there aren't this many account number options stored, add a new option
			if o_i > len(ambiguous_options_lists):
				ambiguous_options_lists.append([print_digits])
			# add this ambiguous option to the options
			# (skip zeroth option - the default digit already recommended in print_digits)
			ambiguous_options_lists[o_i].append(options[o_i+1])
			

	# return the concatenated number and the status code
	return (print_digits, status)

# determine if digit is off by only one segment
# implemented because scanner reportedly adds/drops pipes and underscores
def check_segs_offbyone (num_a):

	# store 7seg index subbars where each 7seg differs from num_a by one char
	found_oneoffs = []

	# added to check if the passed-in array itself matches a number
	original_number = []

	# compare each of three seg pieces in passed-in a
	for i in range(3):
		piece = num_a[i]

		# compare to each seg in valid segment array
		for seg in segs:

			# store segs just one char distance off from piece
			oneoff_pattern = '^([ |_]%s%s|%s[ |_]%s|%s%s[ |_]{1}$)' % \
				(piece[1], piece[2], piece[0], piece[2], piece[0], piece[1])
			matched = re.match (oneoff_pattern, seg)

			# build oneoff digit array from original and this differing segment
			if matched:
				new_segs = num_a[:]
				new_segs[i] = seg
				
				# see if match is valid segs and represents a seven-seg number
				try:
					new_indices = [segs.index(s) for s in new_segs]
					# the matched segments are a number
					if new_indices in seven_segments:
						# the matched number is the old passed-in number
						if new_segs == num_a:
							original_number = new_indices
						# the matched number is a new number
						elif new_indices not in found_oneoffs:
							found_oneoffs.append(new_indices)
						# the matched number was previously accounted for
						else:
							pass
				# the match did not find a number
				except:
					pass

	# if the passed-in array matches a number, put it at the front
	if original_number in seven_segments:
		found_oneoffs.insert(0, original_number)

	print (found_oneoffs)
	# report back how many good off-by-one numeral options were found
	return found_oneoffs

# open file and read lines
class ReadWriteFile:
	def __init__ (self, src, out):
		self.src = src
		self.out = out
	
	def output (self):
		nums = []
		# write to another file
		with open(self.out, "w") as fout, open(self.src, 'r') as fin:
			found_lineset = []
			for l in fin:
				if len(l)>2 and l[0:3] in segs:
					# TODO check for \n or other characters; test len matches
					found_lineset.append(l)
					# turn 3 lines of segs into a single digit row
					if len(found_lineset)>2:
						line_segs = []
						# rip each line in threes
						for i in range ( 0, int(len(l)/3) ):
							
							# cut this line 
							line_0_segs = found_lineset[0] [i*3:(i+1)*3]
							line_1_segs = found_lineset[1] [i*3:(i+1)*3]
							line_2_segs = found_lineset[2] [i*3:(i+1)*3]

							# check line-end segs for missing whitespace and
							# add spaces to treat it as a full 3-char seg line
							if i*3 >= len(found_lineset[0]) and len(line_0_segs)<3:
								line_0_segs += ' '*(3-len(line_0_segs))

							# store index in segs
							a = []
							# three from line+0 -> index in segs -> a[0]
							a.append (line_0_segs)
							# three from line+1 -> index in segs -> a[1]
							a.append (line_1_segs)
							# three from line+2 -> index in segs -> a[2]
							a.append (line_2_segs)
							# a[0:3] -> nested into [line[a]]
							line_segs.append (a)
						# clear this set of 3 lines since digit row
						found_lineset = []
						# append line[a] -> all_nums_a[]
						# translate set of 3 lines with valid segments
						digit_line, status = translate_line_to_digits (line_segs)
						# pass or fail checksum and add status comment
						digit_line += checksum(digit_line, status)
						fout.write(digit_line+"\n")
						# store this line in all numbers found
						nums.append (digit_line)
			# account numbers
			print(nums)
		# file automatically closes after generator
		return nums

# TODO
# - Handle line final 7segs like 5 that may end in '|_' instead of expected '|_ '
# - Add array c ambiguous number suggestions to the rather opaque ' AMB' status

txt_in = 'input.txt'
txt_out = 'output.txt'
txt_reader = ReadWriteFile(txt_in,txt_out)
txt_reader.output()