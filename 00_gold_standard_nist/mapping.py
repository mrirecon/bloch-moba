#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:47:35 2017

@author: nscho

Script for estimating relaxation parameters from single-echo spin-echo measruements.
"""

import numpy as np
import matplotlib.pyplot as plt
from time import time
from scipy.optimize import curve_fit

import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

def T2_func(x, a, b):
    return a * np.exp( -1 / b * x )

def T1_func(x, a, b, c):
    return np.abs( a * ( 1 - np.exp( -1 / b * x + c ) ) )


class mapping(object):
    
    def getmap(self, data):
        
        max_dim = np.shape(data)
        
        #get storage
        store = np.zeros((max_dim[0], max_dim[1], 4)) # 4 = 2 parameter-space with 2 error space
        
        #get time steps
        end = self.st + max_dim[2] * self.dt
        
        time = np.linspace(self.st, end,  max_dim[2], endpoint=False)
        
        for x in range(0, max_dim[0] ):       
            for y in range(0, max_dim[1]):
                    
                print("Pixel: ("+str(x)+", "+str(y)+")")
                
                signal = data[x, y, :]
                
                #Do fitting
                if (self.para == "T2"):
                    popt, pcov = curve_fit(T2_func, time, signal, p0=(1, 0.1))
                    
                elif (self.para == "T1"):
                    try:
                        popt, pcov = curve_fit(T1_func, time, signal, p0=(1, 1, 1))
                    except RuntimeError:
                        store[x, y, 0] = 0
                        store[x, y, 1] = 0
                        store[x, y, 2] = 0
                        store[x, y, 3] = 0
                        continue

                else:
                    print("No parameter is chosen! Please specify one!")
                    raise
                
                print(np.shape(popt))
                
                #calculate error
                perr = np.sqrt(np.diag(pcov))
                    
                #Store data
                store[x, y, 0] = popt[0]
                store[x, y, 1] = popt[1]
                store[x, y, 2] = perr[0] 
                store[x, y, 3] = perr[1]
        
        return store
    
   
        
    def __init__(self, infile, para, st, dt, outfile):
        self.infile = sys.argv[1]
        self.para = sys.argv[2]
        self.st = float(sys.argv[3])
        self.dt = float(sys.argv[4])
        self.outfile = sys.argv[5]
        
        start = time()

        
        self.oridata = np.array(cfl.readcfl(self.infile).squeeze()) #dim = [x, y, time, slice]

        self.map = self.getmap(np.abs(self.oridata))
     
        cfl.writecfl(self.outfile, self.map)
        
        end = time()
        print("Ellapsed time: " + str(end - start) + " s")


        
if __name__ == "__main__":
    #Error if wrong number of parameters
    if( len(sys.argv) != 6):
        print( "Function for creating T1 and T2 maps from cfl image." )
        print( "Usage: mapping.py <infile> <maptype(T1 or T2> <start time> <time difference between frames> <outfile>" )
        exit()
        
    mapping( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] )