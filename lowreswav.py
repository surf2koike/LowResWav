# This work is licensed under CC0 1.0 Universal (Public Domain Dedication).
# To view a copy of this license, visit http://creativecommons.org/publicdomain/zero/1.0/
#
# lowreswav.py - create lower resolution wav files from a source wav file
#
# author : surf2koike
# blog: http://surf2koike.fc2.blog.com/
#
import sys
import os
import numpy as np
import wavio

version = 0.01

def lowreswav(infilename):
	try:
		# read an original wav file
		wr = wavio.read(infilename)
		fs = wr.rate
		width = wr.sampwidth
		bit = {2: 16, 3: 24}.get(width, 0)
		if bit == 0:
			print("Unsupported bit depth")
			return
		data = wr.data
		ch = len(wr.data[0, :])
		print(f"ch:{ch}, bit:{bit}, fs:{fs}")

		res = bit
		while res >= 8:
			# degrade resolution
			if res < bit:
				shift = 2 ** (bit - res)
				fshifted = data / shift
				degraded = fshifted.astype(int) * shift
			else:
				degraded = data

			# write a lower resolution wav file
			splitpath = os.path.splitext(infilename)
			outfilename = f"{splitpath[0]}_{res:02d}{splitpath[1]}"
			print(outfilename)
			wavio.write(outfilename, degraded, fs, sampwidth=width)
			res -= 1

	except Exception as e:
		print(f"Error: {e}")

if __name__ == "__main__":
	args = sys.argv
	if len(args) != 2:
		print(f"lowreswav.py ver. {version}")
		print(f"    Usage: python3 {args[0]} filename")
	else:
		print(args[1])
		lowreswav(args[1])
