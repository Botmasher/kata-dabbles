#!usr/bin/python
# -*- coding: utf-8 -*-

## 	BANK OCR KATA
## 	Josh (Botmasher) playing thru stories found here
## 	https://github.com/testdouble/contributing-tests/wiki/Bank-OCR-kata
##

# Naïve: Hash of seven-segment representation of digits 0-9
# Upgrade: compare seven-segment to alphanum, probability of character match, offer guess
segs = [ '   ', ' _ ', '  |' , '|_ ' , ' _|' , '| |', '|_|' ]
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

# turn nested arrays of triple segments into digits
def translate_to_digits (line):
	line_digits = []
	print_digits = ''
	for a in line:
		# find indices of seg pattern then find digit corresponding to that pattern
		try:
			seg_indices = [ segs.index(a[0]),segs.index(a[1]),segs.index(a[2]) ]
			num = seven_segments.index(seg_indices)
			# store in both array and string
			line_digits.append(num)
			print_digits += str(num)
		# not an array of 3 segments
		except:
			pass
	# return as both array and string
	#return (line_digits, print_digits)
	# just return string since only this implemented below
	return print_digits

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
						digit_line = translate_to_digits (line_segs)
						fout.write(digit_line+"\n")
						# store this line in all numbers found
						nums.append (digit_line)
			# write something after iterating
			print(nums)
		# file automatically closes after with

txt_in = 'input.txt'
txt_out = 'output.txt'
txt_reader = ReadWriteFile(txt_in,txt_out)
txt_reader.output()