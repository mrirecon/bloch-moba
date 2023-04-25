#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 09:00:04 2018

@author: nscho
"""
from contextlib import redirect_stderr
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

from colorsys import hls_to_rgb

import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

# Global variables

FS=35

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'k', 'w']

DARK = 0 #dark layout?

VMIN = 0
VMAX_T1 = 2
VMAX_COIL = 3


DIFF_SCALING = 40

BCOLOR='white'  # Background color
TCOLOR='black'  # Text color


def get_color_channels(mag, phase):

	red =   mag * (1 + np.sin(phase + 0 * 2 * np.pi / 3)) / 2
	green = mag * (1 + np.sin(phase + 1 * 2 * np.pi / 3)) / 2
	blue =  mag * (1 + np.sin(phase + 2 * 2 * np.pi / 3)) / 2

	return red, green, blue


def colorize(z, scale=1):

	mag = scale * np.abs(z)
	phase = np.angle(z) 

	red, green, blue = get_color_channels(mag, phase)

	image = np.stack((red, green, blue), axis=2)

	return image



if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) != 6):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: create_figure.py <LL T1 map> <Bloch T1 map> <outfile> <ROI 1> ... <ROI N>" )
		exit()

	sysargs = sys.argv

	# Load maps        
	t1 = np.abs(cfl.readcfl(sysargs[1]).squeeze())
	t1[t1 == np.inf] = 0

	m0 = cfl.readcfl(sysargs[2]).squeeze()
	m0[m0 == np.inf] = 0

	fa = np.abs(cfl.readcfl(sysargs[3]).squeeze())
	fa[fa == np.inf] = 0

	sens = cfl.readcfl(sysargs[4]).squeeze()
	sens[sens == np.inf] = 0

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

	my_cmap2 = copy.copy(cm.get_cmap('gray'))
	my_cmap2.set_bad(BCOLOR)


	# Create phase colormap
	phase = np.linspace(0, 2*np.pi, 256)

	red, green, blue = get_color_channels(1, phase)
	ones = np.ones(256)

	own_color = np.stack([red, green, blue, ones], axis=1)
	newcmp = colors.ListedColormap(own_color)
	newcmp.set_bad(BCOLOR)



	fig = plt.figure(num = 1, figsize=(40, 10), dpi=120, edgecolor='w')

	outer = gridspec.GridSpec(1, 2, wspace=0.1, hspace=0)

	left = gridspec.GridSpecFromSubplotSpec(1, 2,
			subplot_spec=outer[0], wspace=0.1, hspace=0)

	# --------------------------------------
	#              M0 map
	# --------------------------------------

	ax1 = plt.Subplot(fig, left[0])

	# Layer with image

	# Scale M0 to avoid RGBA values larger than 1
	scale_m0 = 1/np.max(np.abs(m0), axis=(0,1))
	m0_m = m0 * scale_m0

	ima = ax1.imshow(np.abs(m0), origin='lower', cmap=my_cmap2)

	imb = ax1.imshow(colorize(m0_m), origin='lower', cmap=newcmp, vmax=2*np.pi) # vmax just a label here

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("left", size="5%", pad=1.4)
	cax2 = divider.append_axes("right", size="5%", pad=0.05)
	
	# Colorbar 1
	cbar = plt.colorbar(ima, cax=cax, orientation="vertical")
	cbar.set_label("Magnitude / a.u.", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	# Colorbar 2
	cbar = plt.colorbar(imb, cax=cax2)
	cbar.set_label("Phase / rad", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)



	ax1.set_title("M$_0$", fontsize=FS)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')
	# ax1.set_axis_off()

	fig.add_subplot(ax1)

	# --------------------------------------
	#           Bloch FA map
	# --------------------------------------

	ax2 = plt.Subplot(fig, left[1])

	fa_m = np.ma.masked_equal(fa, 0)

	im2 = ax2.imshow(fa_m, origin='lower', cmap=my_cmap)

	divider2 = make_axes_locatable(ax2)
	cax = divider2.append_axes("left", size="5%", pad=1.2)
	cax2 = divider2.append_axes("right", size="5%", pad=0.05)
	cax.set_axis_off()

	# Colorbar 2
	cbar4 = plt.colorbar(im2, cax=cax2)
	# cbar.set_label("Phase / rad", fontsize=FS)
	cbar4.ax.tick_params(labelsize=FS)

	ax2.set_title("FA/FA$_{nom}$", fontsize=FS)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	fig.add_subplot(ax2)


	right = gridspec.GridSpecFromSubplotSpec(1, 4,
			subplot_spec=outer[1], wspace=-0.2, hspace=0)
	
	# --------------------------------------
	#           Add Coil Profiles
	# --------------------------------------
	scale_sens = 1/np.max(np.abs(sens), axis=(0,1,2))

	for i in range(0, np.shape(sens)[2]):

		ax2 = plt.Subplot(fig,  right[i])

		# Scale M0 to avoid RGBA values larger than 1
		sens_m = sens * scale_sens

		im2a = ax2.imshow(np.abs(sens[:,:,i]), origin='lower', cmap=my_cmap2)

		im2b = ax2.imshow(colorize(sens_m[:,:,i]), origin='lower', cmap=newcmp, vmax=2*np.pi)

		# Ensure same scaling as map with colorbar has
		divider = make_axes_locatable(ax2)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cax.set_visible(False)
		cax2 = divider.append_axes("right", size="5%", pad=1.1)
		cax2.set_visible(False)

		ax2.set_title("Sens. #"+str(i), fontsize=FS)

		ax2.set_yticklabels([])
		ax2.set_xticklabels([])
		ax2.xaxis.set_ticks_position('none')
		ax2.yaxis.set_ticks_position('none')
		# ax2.set_axis_off()

		fig.add_subplot(ax2)

	cax.set_visible(True)
	cax2.set_visible(True)

	# Colorbar 1
	cbar = plt.colorbar(ima, cax=cax)
	cbar.set_label("Magnitude / a.u.", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	# Colorbar 2
	cbar = plt.colorbar(imb, cax=cax2)
	cbar.set_label("Phase / rad", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)
	
	fig.savefig(outfile + ".png", bbox_inches='tight', transparent=False)
