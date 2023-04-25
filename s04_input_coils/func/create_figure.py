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

FS=28

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'k', 'w']

DARK = 0 #dark layout?

VMAX = 2.9
VMAX2 = 0.08
VMIN = 0

DIFF_SCALING = 1


BCOLOR='white'  # Background color
TCOLOR='black'  # Text color



def perform_roi_analysis(paramap, roi):

	segment = paramap * roi

	# Set zeros to be invalid for mean calculation
	segment_m = np.ma.masked_equal(segment, 0)

	return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) == 7):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: create_figure.py <Bloch T1 map> <Bloch T2 map> <Bloch T1 map 1> <Bloch T2 map 2>  <outfile>" )
		exit()

	sysargs = sys.argv

	# Load maps
	
	bloch_1_t1 = np.abs(cfl.readcfl(sysargs[1]).squeeze())
	bloch_1_t1[bloch_1_t1 == np.inf] = 0

	bloch_1_t2 = np.abs(cfl.readcfl(sysargs[2]).squeeze())
	bloch_1_t2[bloch_1_t2 == np.inf] = 0

	bloch_2_t1 = np.abs(cfl.readcfl(sysargs[3]).squeeze())
	bloch_2_t1[bloch_2_t1 == np.inf] = 0

	bloch_2_t2 = np.abs(cfl.readcfl(sysargs[4]).squeeze())
	bloch_2_t2[bloch_2_t2 == np.inf] = 0


	# Define output filename
	outfile = sysargs[5]

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
	


	fig = plt.figure(num = 1, figsize=(15, 15), dpi=120, edgecolor='w')

	outer = gridspec.GridSpec(1, 2, wspace=0, hspace=0, figure=fig)

	left = gridspec.GridSpecFromSubplotSpec(2, 1,
			subplot_spec=outer[0], wspace=0, hspace=0)
	

	# --------------------------------------
	#           Bloch T1 map 1
	# --------------------------------------

	ax2 = plt.Subplot(fig, left[0])

	bloch_1_t1m = np.ma.masked_equal(bloch_1_t1, 0)

	im2 = ax2.imshow(bloch_1_t1m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax2)
	cax = divider.append_axes("bottom", size="5%", pad=0.05)
	cax.set_visible(False)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	ax2.set_title("T$_1$ from IR bSSFP", fontsize=FS+5)
	ax2.set_ylabel("With Regularization", fontsize=FS+5)
	# ax2.set_ylabel("short RF", fontsize=FS)

	# ax2.text(0.03*np.shape(bloch_1_t1m)[0], 0.03*np.shape(bloch_1_t1m)[0], '$\\bf{T}_{1,B}$', fontsize=FS+5, color=TCOLOR)

	fig.add_subplot(ax2)

	# --------------------------------------
	#           Bloch T1 map 2
	# --------------------------------------

	ax2 = plt.Subplot(fig, left[1])

	bloch_2_t1m = np.ma.masked_equal(bloch_2_t1, 0)

	im2 = ax2.imshow(bloch_2_t1m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	divider = make_axes_locatable(ax2)
	cax = divider.append_axes("bottom", size="5%", pad=0.05)
	cbar = plt.colorbar(im2, cax=cax, orientation="horizontal")
	cbar.set_label("T$_1$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	ax2.set_ylabel("No Regularization", fontsize=FS+5)

	# ax2.text(0.03*np.shape(bloch_2_t1m)[0], 0.03*np.shape(bloch_2_t1m)[0], '$\\bf{T}_{1,B}$', fontsize=FS+5, color=TCOLOR)

	fig.add_subplot(ax2)

	# --------------------------------------
	#           Bloch T2 map short
	# --------------------------------------

	right = gridspec.GridSpecFromSubplotSpec(2, 1,
			subplot_spec=outer[1], wspace=0, hspace=0)

	ax2 = plt.Subplot(fig, right[0])

	bloch_1_t2m = np.ma.masked_equal(bloch_1_t2, 0)

	im2 = ax2.imshow(bloch_1_t2m, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax2)
	cax = divider.append_axes("bottom", size="5%", pad=0.05)
	cax.set_visible(False)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	ax2.set_title("T$_2$ from IR bSSFP", fontsize=FS+5)

	# ax2.text(0.03*np.shape(bloch_1_t2m)[0], 0.03*np.shape(bloch_1_t2m)[0], '$\\bf{T}_2$', fontsize=FS+5, color=TCOLOR)

	# ax2.set_ylabel("short RF", fontsize=FS)

	fig.add_subplot(ax2)

	# --------------------------------------
	#           Bloch T2 map long
	# --------------------------------------

	ax2 = plt.Subplot(fig, right[1])

	bloch_2_t2m = np.ma.masked_equal(bloch_2_t2, 0)

	im2 = ax2.imshow(bloch_2_t2m, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

	divider = make_axes_locatable(ax2)
	cax = divider.append_axes("bottom", size="5%", pad=0.05)
	cbar = plt.colorbar(im2, cax=cax, orientation="horizontal")
	cbar.set_label("T$_2$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	# ax2.text(0.03*np.shape(bloch_2_t2m)[0], 0.03*np.shape(bloch_2_t2m)[0], '$\\bf{T}_2$', fontsize=FS+5, color=TCOLOR)

	fig.add_subplot(ax2)


	fig.savefig(outfile + '.png', bbox_inches='tight', transparent=False)