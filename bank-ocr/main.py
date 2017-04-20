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

# open file and read lines
class ReadWriteFile:
	def __init__ (self, src, out):
		self.src = src
		self.out = out
	
	def output (self):
		found_lines = []
		count = 0
		numbers
		# write to another file
		with open(self.out, "w") as fout, open(self.src, 'r') as fin:
			for l in fin:
				count += 1
				if count not in found_lines and len(l)>0 and l[0:3] in segs:
					l_len = len(fin[count])
					if l_len == len(fin[count+1]) and l_len == len(fin[count+2]):
						found_lines.append(count)
						found_lines.append(count + 1)
						found_lines.append(count + 2)
						# rip each line in threes
						for r in range (0,len(l)-1):
						# store index in segs
							# three from line+0 -> index in segs -> a[0]
							# three from line+1 -> index in segs -> a[1]
							# three from line+2 -> index in segs -> a[2]
							# a[0:3] -> nested into line[a]
							# append line[a] -> all_nums_a[]
						# now your all_nums_a can be switched back and forth
				# print per line
				fout.write ( "%s : %s\n" % (l.rstrip('\n'), found_numline) )
			# write something after iterating
			fout.write ( "Final finding :  %s" % (found_numline) )
		# file automatically closes after with?
txt_in = 'input.txt'
txt_out = 'output.txt'
txt_reader = ReadWriteFile(txt_in,txt_out)
txt_reader.output()
# - identify chunks (first line with only pattern [0] or [1])
# - cut chunks at last line (3)
# - hold chunk in memory while cutting top,mid,bottom line into n subsegs
# - verify that the subsegs line up
# - combine subsegs into segs
# - turn segs into array
# - find array in seven_segments -> that index is the digit
# - return int(string) of all digits in that chunk
# - go thru file until last chunk completed