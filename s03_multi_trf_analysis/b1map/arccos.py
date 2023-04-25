#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nscho
"""
import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

import numpy as np


if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) != 3):
		print( "arccos(input)" )
		print( "#-----------------------------------------------" )
		print( "Usage: arccos.py <input> <output>" )
		exit()

	sysargs = sys.argv

	out = np.arccos(cfl.readcfl(sysargs[1]).squeeze())

	# Load input
	cfl.writecfl(sysargs[2], out)
	