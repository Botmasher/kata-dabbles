#!usr/bin/python
# -*- coding: utf-8 -*-

## 	BANK OCR KATA
## 	Josh (Botmasher) playing thru stories found here
## 	https://github.com/testdouble/contributing-tests/wiki/Bank-OCR-kata
##

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

# not yet implemented; not used below
def translate_to_indices_array (segs_a):
	return None

# not yet tested; not used below
def translate_to_indices (a):
	if a in seven_segments:
		return seven_segments.index(a)
	else:
		return None

# check for well-formed account numbers
def checksum (acct_num):
	if '?' in acct_num:
		return ' ILL'
	sum_val = sum( int(acct_num[i])*i for i in range(len(acct_num)) )
	if sum_val%11 == 0:
		return ''
	return ' ERR'

# turn single seven segments array into an integer
def translate_seven_segments (a):
	# find indices of seg pattern then numeral corresponding to pattern
	try:
		seg_indices = [ segs.index(a[0]),segs.index(a[1]),segs.index(a[2]) ]
		num = seven_segments.index(seg_indices)
		return str(num)
	# the segment pattern did not match a numeral
	except:
		return '?'

# turn nested line arrays of triple segments into account number digits
# built around seven segs translation function above
def translate_line_to_digits (line):
	print_digits = ''
	# each subarray contains 3 segment sections to be read as one numeral
	for a in line:
		num = translate_seven_segments(a)
		# build account number string
		print_digits += str(num)
	# just return string since only this implemented below
	return print_digits

# determine if digit is off by only one segment
# implemented because scanner reportedly adds/drops pipes and underscores
def check_segs_offbyone (num_a):

	# store 7seg index subbars where each 7seg differs from num_a by one char
	found_oneoffs = []

	# compare each of three seg pieces in passed-in a
	for i in range(3):

		# compare to each seg in valid segment array
		for seg in segs:

			# store segs just one char distance off from piece
			oneoff_pattern = '^([ |_]%s%s|%s[ |_]%s|%s%s[ |_])' % \
				(piece[1], piece[2], piece[0], piece[2], piece[0], piece[1])
			matched = re.match (oneoff_pattern, seg)

			# build oneoff digit array from original and this differing segment
			if matched:
				new_oneoff = num_a
				new_oneoff[i] = segs.index(seg)

			# the oneoff segments are really a digit, store as a find
			if matched and new_oneoff in seven_segments:
				found_oneoffs.append(new_oneoff)

	# report back how many good off-by-one numeral options were found
	return found_oneoffs
	# - if none were found, this also needs to be reported back (or empty array)
	# - the parent func may use this to suggest " AMB" (multiple options)
	# - or may use this to report " ILL" (no options, including original a)
# now use this function during checksum to determine if an acct num is " AMB"
# if no numbers are possible it is still just " ILL"

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
					# /!\ TODO check for \n or other characters; test len matches
					found_lineset.append(l)
					# turn 3 lines of segs into a single digit row
					if len(found_lineset)>2:
						line_segs = []
						# rip each line in threes
						for i in range ( 0, int(len(l)/3) ):
							# store index in segs
							a = []
							# three from line+0 -> index in segs -> a[0]
							a.append ( found_lineset[0] [i*3:(i+1)*3] )
							# three from line+1 -> index in segs -> a[1]
							a.append ( found_lineset[1] [i*3:(i+1)*3] )
							# three from line+2 -> index in segs -> a[2]
							a.append ( found_lineset[2] [i*3:(i+1)*3] )
							# a[0:3] -> nested into [line[a]]
							line_segs.append (a)
						# clear this set of 3 lines since digit row
						found_lineset = []
						# append line[a] -> all_nums_a[]
						# translate set of 3 lines with valid segments
						digit_line = translate_line_to_digits (line_segs)
						# add status comment if acct number fails checksum
						digit_line += checksum(digit_line)
						fout.write(digit_line+"\n")
						# store this line in all numbers found
						nums.append (digit_line)
			#for i in range(0,len(nums)):
			#	print(checksum(nums[i]))
			# write something after iterating
			print(nums)
		# file automatically closes after with

# Handle line final 7segs like 5 that may end in '|_' instead of expected '|_ '

txt_in = 'input.txt'
txt_out = 'output.txt'
txt_reader = ReadWriteFile(txt_in,txt_out)
txt_reader.output()