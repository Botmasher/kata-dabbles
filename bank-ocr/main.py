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

class Seven_Segment:
	# all valid segs for making a numeral
	segs = [ '   ' , ' _ ' , '  |' , '|_ ' , ' _|' , '| |' , '|_|' ]
	# segs indices for forming numerals 0 to 9
	indices = [ \
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

	def __init__ (self):
		return self

	# translate a single digit into seven segs
	def num_to_segs (self, numeral):
		if type(numeral) is int and len(str(numeral)) == 1:
			num_seg_indices = self.indices[numeral]
			num_segs = [ self.segs[num_seg_indices[n]] for n in num_seg_indices ]
			return num_segs
		return None

	# translate seven segments into a single digit
	def segs_to_num (self, segments):
		# find seg indices then find the number they represent
		try:
			indices = self.segs_to_indices (segments)
			return self.indices.index(indices)
		# not a seven-segment representation of a number
		except:
			return None

	# translate seven segments into segs indices
	def segs_to_indices (self, segments):
		# find seg indices then find the number they represent
		try:
			return [ self.segs.index(segments[i]) for i in range(3) ]
		# not a seven-segment representation of a number
		except:
			return None

	# translate segs indices into seven segments
	def indices_to_segs (self, indices):
		try:
			return [ self.segs[indices[i]] for i in range(3) ]
		# not a seven-segment representation of a number
		except:
			return None

sgmt = Seven_Segment()


# check for well-formed account numbers
def checksum (acct_num, status_code):
	ambiguous = ' AMB'
	sum_val = None
	if '?' not in acct_num:
		sum_val = sum( int(acct_num[i])*i for i in range(len(acct_num)) )
	if sum_val and sum_val%11 == 0 or ambiguous in status_code:
		return status_code
	return ' ERR'

# turn nested line arrays of triple segments into account number digits
# depends on seven segs off-by-one function
def translate_line_to_digits (line):
	# account num strings to build and return
	print_digits = ''
	status = ''
	# characters introduced into acct num string
	illegible_wildcard = '?'
	ambiguous = ' AMB'
	illegible = ' ILL'
	# characters to be replaced in acct num string
	blank_char = 'X'
	# storage for alternative acct num options found
	ambiguous_options_lists = []

	# build ambiguous options placeholders
	for i in range (10):
		ambiguous_options_lists.append([blank_char for l in line])

	# each subarray contains 3 segment sections to be read as one numeral
	for i in range(len(line)):

		segment_array = line[i]

		# find how many numbers this array can represent
		options = check_segs_offbyone(segment_array)

		## Build account number string from options

		# translate options into numerals
		options = [seven_segments.index(n) for n in options]

		# unambiguous or ambiguous and represents a number
		if len(options) >= 1:
			this_digit = str(options[0])
		# unambiguous and does not represent a number
		else:
			status = illegible
			this_digit = illegible_wildcard

		# add this number to final account number
		print_digits += this_digit

		# 'ambiguous' status (does not override 'illegible' status)
		if len(options) > 1 and illegible_wildcard not in print_digits:
			status = ambiguous
		
		# store extra options
		new_options = options[1:]
		for opt_i in range(len(new_options)):
			if opt_i < len(ambiguous_options_lists):
				print(ambiguous_options_lists[opt_i])
				# replace X with digit options at this spot in the acct num
				ambiguous_options_lists[opt_i][i] = str(new_options[opt_i])
			else:
				# too many options - we are not tracking this many options
				pass
	
	# clean up options and append to AMB
	if status == ambiguous:
		used_options = []
		status += ' ['
		for opt in ambiguous_options_lists:
			# chuck any options that are still blank (unfilled/not replaced)
			if opt and all(e==blank_char for e in opt):
				pass
			# replace any that are partially blank with print_digit[i]
			elif opt not in used_options:
				for char_i in range(len(opt)):
					if opt[char_i] == blank_char:
						opt[char_i] = print_digits[char_i]
				# join character array into single acct num recommendation string
				# we now have an option to append to AMB status
				status += "%s, " % "".join(opt)
				used_options.append(opt)
			# this option already used
			else:
				pass
		status = status[:-2]+']'
	print (print_digits + status)
	# return the concatenated number and the status code
	return (print_digits, status)

# go through list and verify that elements are keys in a dictionary
def list_elements_are_keys_in_hash (l, h):
	if len(l) == 1:
		return l[0] in h
	return (l[0] in h and list_elements_are_keys_in_hash(l[1:], h))

# determine if digit is off by only one segment
# implemented because scanner reportedly adds/drops pipes and underscores
def check_segs_offbyone (num_a):

	# store 7seg index subbars where each 7seg differs from num_a by one char
	found_oneoffs = []
	found_original = False

	# build oneoff dictionary by eye instead of regexing patterns for now
	oneoff_hash = {}
	# segs are 0:'   ',1:' _ ',2:'  |',3:'|_ ',4:' _|',5:'| |',6:'|_|'
	oneoff_hash[segs[0]] = [segs[0], segs[1], segs[2]]
	oneoff_hash[segs[1]] = [segs[1], segs[0], segs[3], segs[4]]
	oneoff_hash[segs[2]] = [segs[2], segs[0], segs[4], segs[5]]
	oneoff_hash[segs[3]] = [segs[3], segs[1], segs[6]]
	oneoff_hash[segs[4]] = [segs[4], segs[1], segs[2], segs[6]]
	oneoff_hash[segs[5]] = [segs[5], segs[2], segs[6]]
	oneoff_hash[segs[6]] = [segs[6], segs[3], segs[4], segs[5]]

	# guard against faulty num/seg array
	if len(num_a) != 3 or not list_elements_are_keys_in_hash(num_a, oneoff_hash):
		return []

	# go through each passed in segment and look up each of its oneoffs
	for i in range(len(num_a)):
		for oneoff_seg in oneoff_hash[num_a[i]]:
			# compose segment permutation and translate into seg indices
			new_segs = num_a[:]
			new_segs[i] = oneoff_seg
			new_num = [segs.index(s) for s in new_segs]
			# this permutation is the original segs and is indeed a 7-seg num
			if new_num in seven_segments and new_segs == num_a and not found_original:
				# save to place up front at the end
				found_oneoffs.insert(0, new_num)
				found_original = True
			# this permutation matches a new 7-seg num
			elif new_num in seven_segments and new_segs != num_a:
				found_oneoffs.append(new_num)
			# this permutation is not a 7-segment representation of a number
			else:
				pass

	print (found_oneoffs)
	# report back how many good off-by-one numeral options were found
	# (including the original at index 0 if it was also a number)
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

txt_in = 'input.txt'
txt_out = 'output.txt'
txt_reader = ReadWriteFile(txt_in,txt_out)
txt_reader.output()