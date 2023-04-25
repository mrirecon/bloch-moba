#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.optimize import curve_fit

from math import ceil


import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

def func(x, m, b):
	return m * x + b


# Global variables

FS=20

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'peru', 'palegreen', 'slategray', 'gold', 'springgreen', 'slateblue', 'maroon']

DARK = 0 #dark layout?

VMAX = 4
VMAX2 = 0.7
VMIN = 0

DIFF_SCALING = 10


BCOLOR='white'  # Background color
TCOLOR='black'  # Text color



def perform_roi_analysis(paramap, roi):

	segment = paramap * roi

	# Set zeros to be invalid for mean calculation
	segment_m = np.ma.masked_equal(segment, 0)

	return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) == 6):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: create_figure.py <LL ref T1> <T1 maps> <outfile> <wav [txt]>" )
		exit()

	sysargs = sys.argv

	# Load maps
	reft1 = np.abs(cfl.readcfl(sysargs[1]).squeeze())
	reft1[reft1 == np.inf] = 0

	t1 = np.abs(cfl.readcfl(sysargs[2]).squeeze())
	t1[t1 == np.inf] = 0

	# Define output filename
	outfile = sysargs[3]

	fa = np.loadtxt(sysargs[4], unpack=True)


	# DIMS
	dims = np.shape(t1)	# Samples, Samples, sR1, sR2
	print(dims)

	# --------------------------------------
	#         Create visualization
	# --------------------------------------

	if "DARK_LAYOUT" in os.environ:
		DARK = int(os.environ["DARK_LAYOUT"])

	if(DARK):
		plt.style.use(['dark_background'])
		BCOLOR='black'
		TCOLOR='white'
	else:
		plt.style.use(['default'])

	my_cmap = copy.copy(cm.get_cmap('viridis'))
	my_cmap.set_bad(BCOLOR)

	my_cmap2 = copy.copy(cm.get_cmap('turbo'))
	my_cmap2.set_bad(BCOLOR)


	fig = plt.figure(num = 1, figsize=(55, 10), dpi=120, edgecolor='w')

	
	
	
	outer = gridspec.GridSpec(1, 2, wspace=-0.4, hspace=0, figure=fig)

	left = gridspec.GridSpecFromSubplotSpec(3, 1,
			subplot_spec=outer[0], wspace=0, hspace=0,
			height_ratios=(0.3,0.4,0.3))

	# LL reference T1 map

	ax1 = fig.add_subplot(left[1])

	t1m = np.ma.masked_equal(reft1, 0)

	im = ax1.imshow(t1m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	cbar.set_label("T$_1$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS-5)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')
	# ax1.set_axis_off()

	ax1.set_title("Look-Locker\nReference", fontsize=FS+5)

	ax1.text(0.03*np.shape(t1m)[0], 0.03*np.shape(t1m)[0], '$\\bf{T}_{1,LL}$', fontsize=FS, color=TCOLOR)

	fig.add_subplot(ax1)


	# Bloch T1 map

	grid = gridspec.GridSpecFromSubplotSpec(2, dims[2],
		subplot_spec=outer[1], wspace=0.1, hspace=-0.1)


	for i in range(0, dims[2]):

		ax1 = fig.add_subplot(grid[i])

		t1m = np.ma.masked_equal(t1[:,:,i], 0)

		im = ax1.imshow(t1m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

		divider = make_axes_locatable(ax1)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cax.set_visible(False)

		ax1.set_yticklabels([])
		ax1.set_xticklabels([])
		ax1.xaxis.set_ticks_position('none')
		ax1.yaxis.set_ticks_position('none')
		# ax1.set_axis_off()

		if (0 == i):
			ax1.set_title("\u03B2$_0$: "+str(fa[i]), fontsize=FS+5)
			ax1.set_ylabel("Bloch Model", fontsize=FS)
		else:
			ax1.set_title(str(fa[i]), fontsize=FS+5)

		ax1.text(0.03*np.shape(t1m)[0], 0.03*np.shape(t1m)[0], '$\\bf{T}_{1,\u03B2_0}$', fontsize=FS, color=TCOLOR)

		fig.add_subplot(ax1)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	cbar.set_label("T$_1$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS-5)


	# Diff T1 map


	for i in range(0, dims[2]):

		ax1 = fig.add_subplot(grid[(dims[2])+i])

		diff = np.abs(reft1-t1[:,:,i]) * DIFF_SCALING

		diffm = np.ma.masked_equal(diff, 0)

		im = ax1.imshow(diffm, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

		divider = make_axes_locatable(ax1)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cax.set_visible(False)

		ax1.set_yticklabels([])
		ax1.set_xticklabels([])
		ax1.xaxis.set_ticks_position('none')
		ax1.yaxis.set_ticks_position('none')
		# ax1.set_axis_off()

		ax1.text(0.03*np.shape(diffm)[0], 0.03*np.shape(diffm)[0], 'x'+str(DIFF_SCALING), fontsize=FS, color=TCOLOR)

		if (0 == i):
			ax1.set_ylabel("Difference", fontsize=FS)

		fig.add_subplot(ax1)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	cbar.set_label("$|\\bf{T}_{1,LL}-\\bf{T}_{1,\u03B2_8}|$ / s", fontsize=FS-2)
	cbar.ax.tick_params(labelsize=FS-5)

	fig.savefig(outfile + '.png', bbox_inches='tight', transparent=False)

