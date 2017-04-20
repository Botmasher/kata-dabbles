#!usr/bin/python
# -*- coding: utf-8 -*-

## 	BANK OCR KATA
## 	Josh (Botmasher) playing thru the "stories" found here
## 	https://github.com/testdouble/contributing-tests/wiki/Bank-OCR-kata
##

# Naïve: Hash of seven-segment representation of digits 0-9
# Upgrade: compare seven-segment to alphanum, probability of character match, offer guess
sgs = [ '   ', ' _ ', '  |' , '|_ ' , ' _|' , '| |', '|_|' ]
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
#	print (sgs[a[0]]+'\n'+sgs[a[1]]+'\n'+sgs[a[2]])

#segments_map = {n: seven_segments[n] for n in range(0,len(seven_segments))}

# - open file
# - read lines
class ReadWriteFile:
	def __init__ (self, src, out):
		self.src = src
		self.out = out
	
	def output (self):
		# write to another file
		with open(self.out, "w") as fout, open(self.src, 'r') as fin:
			for l in fin:
				# do calculations
				# print per line
				fout.write ( l + " : %s \n" % str(1234) )
			# write something total
			fout.write ( "\n Output value :  %s" % (str(1234)) )
		# file automatically closes after with?
txt_reader = ReadWriteFile('testread.txt','testwrite.txt')
txt_reader.output()
txt_filtered = filter(txt_out, 'something to find!')
# - identify chunks (first line with only pattern [0] or [1])
# - cut chunks at last line (3)
# - hold chunk in memory while cutting top,mid,bottom line into n subsegs
# - verify that the subsegs line up
# - combine subsegs into segs
# - turn segs into array
# - find array in seven_segments -> that index is the digit
# - return int(string) of all digits in that chunk
# - go thru file until last chunk completed