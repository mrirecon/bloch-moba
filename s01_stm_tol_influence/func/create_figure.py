#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 09:00:04 2018

@author: nscho
"""
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

# Global variables

FS=20

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'peru', 'palegreen', 'slategray', 'pink', 'springgreen', 'slateblue', 'maroon']

DARK = 0 #dark layout?

VMAX = 2
VMIN = 0

DIFF_SCALING = 20

BCOLOR='white'  # Background color
TCOLOR='black'  # Text color



def perform_roi_analysis(paramap, roi):

	segment = paramap * roi

	# Set zeros to be invalid for mean calculation
	segment_m = np.ma.masked_equal(segment, 0)

	return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) < 6):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: create_figure.py <letter> <title> <tol> <ROIS> <on-resonant Bloch T1> <slice-profile Bloch T1> <outfile>" )
		exit()

	sysargs = sys.argv

	letter = sysargs[1]
	title = sysargs[2]
	tol = np.loadtxt(sysargs[3]+'.txt', unpack=True)

	rois = np.abs(cfl.readcfl(sysargs[4]).squeeze())
	rois[rois == np.inf] = 0

	bloch_maps = np.abs(cfl.readcfl(sysargs[5]).squeeze())
	bloch_maps[bloch_maps == np.inf] = 0

	bloch_mapsSP = np.abs(cfl.readcfl(sysargs[6]).squeeze())
	bloch_mapsSP[bloch_mapsSP == np.inf] = 0

	# Define output filename
	outfile = sysargs[7]

	# --------------------------------------
	#         Create visualization
	# --------------------------------------

	Nplots = np.shape(bloch_maps)[2]

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


	fig = plt.figure(num = 1, figsize=(30, 13), dpi=120, edgecolor='w')
	# fig = plt.figure(num = 1, figsize=(30, 5), dpi=120, edgecolor='w')

	outer = gridspec.GridSpec(1, Nplots, wspace=0, hspace=-0.1)


	# --------------------------------------
	#          Reference map: no SP
	# --------------------------------------

	ref = bloch_maps[:,:,0]

	left = gridspec.GridSpecFromSubplotSpec(2, 1,
		subplot_spec=outer[0], wspace=0, hspace=0)

	ax1 = plt.Subplot(fig, left[0])

	# Layer with image

	ref_m = np.ma.masked_equal(ref, 0)

	im = ax1.imshow(ref_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cax.set_visible(False)

	ax1.set_title("$\\bf{Reference}$ $\\bf{T}$$_1$", fontsize=FS+10)

	ax1.set_ylabel("$\\bf{on-resonant}$", fontsize=FS+10)

	ax1.text(0.25 * np.shape(ref_m)[0], 0.9 * np.shape(ref_m)[0], "tol="+str(tol[0]), fontsize=FS+10, fontweight='bold', color=TCOLOR)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')

	# Figure label "A"
	ax1.text(-0.3*np.shape(ref_m)[0], 1.1*np.shape(ref_m)[0], letter, fontsize=FS+30, fontweight='bold', color=TCOLOR)
	ax1.text(-0.15*np.shape(ref_m)[0], 1.1*np.shape(ref_m)[0], title, fontsize=FS+10, fontweight='bold', color=TCOLOR)

	fig.add_subplot(ax1)

	# --------------------------------------
	#          Reference map: SP
	# --------------------------------------

	ref2 = bloch_mapsSP[:,:,0]

	ax1 = plt.Subplot(fig, left[1])

	# Layer with image

	ref2_m = np.ma.masked_equal(ref2, 0)

	im = ax1.imshow(ref2_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cax.set_visible(False)

	ax1.set_ylabel("$\\bf{slice-profile}$", fontsize=FS+10)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')

	fig.add_subplot(ax1)


	# --------------------------------------
	#           Bloch T1 maps
	# --------------------------------------

	for i in range(1, Nplots):

		print(i)

		middle = gridspec.GridSpecFromSubplotSpec(2, 1,
				subplot_spec=outer[i], wspace=0, hspace=0)

		ax2 = plt.Subplot(fig, middle[0])

		# --------------------------------------
		# Difference between Look-Locker and Bloch T1 map: No SP
		# --------------------------------------

		# Current map
		bloch_map = bloch_maps[:,:,i]

		ax3 = plt.Subplot(fig, middle[0])

		diff_map = np.abs(ref - bloch_map)

		diff_map_m = np.ma.masked_equal(diff_map, 0)

		im3 = ax3.imshow(diff_map_m*DIFF_SCALING, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

		# Add scaling as text to Diff image
		ax3.text(0.01*np.shape(diff_map)[0], 0.01*np.shape(diff_map)[0], 'x'+str(DIFF_SCALING), fontsize=FS+20, color=TCOLOR)

		ax3.text(0.25 * np.shape(diff_map)[0], 0.9 * np.shape(diff_map)[0], "tol="+str(tol[i]), fontsize=FS+10, fontweight='bold', color=TCOLOR)


		divider = make_axes_locatable(ax3)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cbar = plt.colorbar(im3, cax=cax)
		cbar.set_label("T$_1$ / s", fontsize=FS+5)
		cbar.ax.tick_params(labelsize=FS+5)

		if (Nplots - 1 != i):
			cax.set_visible(False)

		if (2 == i):
			ax3.text(0.55 * np.shape(diff_map)[0], 1.05 * np.shape(diff_map)[0], "$\\bf{Difference~Maps}$", fontsize=FS+10, fontweight='bold', color=TCOLOR)
			# ax3.set_title("$\\bf{Diff.~Map}$", fontsize=FS+10)

		ax3.set_yticklabels([])
		ax3.set_xticklabels([])
		ax3.xaxis.set_ticks_position('none')
		ax3.yaxis.set_ticks_position('none')
		# ax3.grid('off')

		fig.add_subplot(ax3)

		# --------------------------------------
		# Difference between Look-Locker and Bloch T1 map: SP
		# --------------------------------------

		# Current map
		bloch_map2 = bloch_mapsSP[:,:,i]

		ax3 = plt.Subplot(fig, middle[1])

		diff_map = np.abs(ref2 - bloch_map2)

		diff_map_m = np.ma.masked_equal(diff_map, 0)

		im3 = ax3.imshow(diff_map_m*DIFF_SCALING, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

		# Add scaling as text to Diff image
		ax3.text(0.01*np.shape(diff_map)[0], 0.01*np.shape(diff_map)[0], 'x'+str(DIFF_SCALING), fontsize=FS+20, color=TCOLOR)

		divider = make_axes_locatable(ax3)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cbar = plt.colorbar(im3, cax=cax)
		cbar.set_label("T$_1$ / s", fontsize=FS+5)
		cbar.ax.tick_params(labelsize=FS+5)

		if (Nplots - 1 != i):
			cax.set_visible(False)

		ax3.set_yticklabels([])
		ax3.set_xticklabels([])
		ax3.xaxis.set_ticks_position('none')
		ax3.yaxis.set_ticks_position('none')
		# ax3.grid('off')

		fig.add_subplot(ax3)

	fig.savefig(outfile + ".png", bbox_inches='tight', transparent=False)
