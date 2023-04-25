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
from scipy.optimize import curve_fit
from math import ceil

import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

# Global variables

FS=25

COLORS = ['r', 'b', 'm', 'maroon']

DARK = 0 #dark layout?

VMAX = 2.8
VMIN = 0

DIFF_SCALING = 20

BCOLOR='white'  # Background color
TCOLOR='black'  # Text color



def perform_roi_analysis(paramap, roi):

	segment = paramap * roi

	# Set zeros to be invalid for mean calculation
	segment_m = np.ma.masked_equal(segment, 0)

	return segment_m.mean(), segment_m.std()

def func(x, a, b, c):
	return 1 / ((a - b) * (1 - np.exp(-c * x)) + b) * np.cos(45/2 * np.pi/180)


if __name__ == "__main__":

	#Error if wrong number of parameters
	if( len(sys.argv) < 4):
		print( "Plotting" )
		print( "#-----------------------------------------------" )
		print( "Usage: create_figure.py <T_RF [txt]> <ROI, 3D> <outfile> <Bloch T1 maps, 2D>" )
		exit()

	sysargs = sys.argv

	trf = np.loadtxt(sysargs[1]+'.txt', unpack=True)

	roi = np.abs(cfl.readcfl(sysargs[2]).squeeze())
	roi[roi == np.inf] = 0

	# Define output filename
	outfile = sysargs[3]

	# Load and stack all passed roi
	print("Passed roi are:")

	bloch_maps = []

	for i in sysargs[4:]:

		print("\t", i)

		bloch_map = np.abs(cfl.readcfl(i).squeeze())
		bloch_map[bloch_map == np.inf] = 0

		bloch_maps.append(bloch_map)


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


	fig = plt.figure(num = 1, figsize=(20, 8), dpi=120, edgecolor='w')

	outer = gridspec.GridSpec(1, 2, wspace=0.15, hspace=0)


	# --------------------------------------
	#          Reference map
	# --------------------------------------

	ref = bloch_maps[0]

	left = gridspec.GridSpecFromSubplotSpec(1, 1,
		subplot_spec=outer[0], wspace=0, hspace=0)

	ax1 = plt.Subplot(fig, left[0])

	# Layer with image

	ref_m = np.ma.masked_equal(ref, 0)

	im = ax1.imshow(ref_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Add Layer with roi
	# First and last roi are not interesting because they are filled with water
	for i in range(0, np.shape(roi)[2]):

		# Single color for ROI
		cmap_roi = colors.ListedColormap(COLORS[i])
		roi_tmp = np.ma.masked_equal(roi[:,:,i], 0)

		# Plot ROI as overlay
		im = ax1.imshow(roi_tmp, origin='lower', cmap=cmap_roi, alpha=0.6)

		# Add arrow pointing to ROI
		ybase = np.max(np.where(1 == roi_tmp)[0])
		xbase = np.max(np.where(1 == roi_tmp)[1])
		ax1.arrow(xbase+25, ybase+25, -12, -12, head_width=10, color=COLORS[i])

	# Recreate Colorbar from image
	im = ax1.imshow(ref_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	# cbar.set_label("T$_1$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS)

	# ax1.set_ylabel("$\\bf{T}$$_1$ $\\bf{map}$", fontsize=FS)

	# ax1.text(0.01 * np.shape(ref_m)[0], 0.01 * np.shape(ref_m)[0], "tol="+str(tol[0]), fontsize=FS+10, fontweight='bold', color=TCOLOR)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')

	# Figure label "A"
	# ax1.text(-0.3*np.shape(ref_m)[0], 1.2*np.shape(ref_m)[0], letter, fontsize=FS+20, fontweight='bold', color=TCOLOR)
	# ax1.text(-0.15*np.shape(ref_m)[0], 1.2*np.shape(ref_m)[0], title, fontsize=FS+10, fontweight='bold', color=TCOLOR)

	fig.add_subplot(ax1)


	# --------------------------------------
	#          ROI Analysis
	# --------------------------------------


	val = []
	std = []

	for i in range(0, np.shape(roi)[2]):

		bval = []
		bstd = []

		for b in bloch_maps:

			tval, tstd = perform_roi_analysis(b, roi[:,:,i])

			bval.append(tval)
			bstd.append(tstd)

		val.append(bval)
		std.append(bstd)

	val = np.array(val)
	std = np.array(std)


	right = gridspec.GridSpecFromSubplotSpec(1, 1,
		subplot_spec=outer[1], wspace=0, hspace=0)

	ax2 = plt.Subplot(fig, right[0])

	para = []
	err = []

	for i in range(0, np.shape(val)[0]):

		# Fit data

		xdata = trf/10
		xcont = np.linspace(min(xdata), max(xdata)+3, 100)

		ydata = val[i]

		popt, pcov = curve_fit(func, xdata, ydata) #, bounds=(0, [3., 1., 0.5]))

		perr = np.sqrt(np.diag(pcov))

		print(popt, perr)

		para.append(popt)
		err.append(perr)

		ax2.errorbar(xdata, ydata, yerr=std[i], fmt='*', color=COLORS[i], label="ROI: "+str(i))

		ax2.plot(xcont, func(xcont, *popt), '--', color=COLORS[i]) # M$_{ss}^{no MT}$=%5.3f, M$_{ss}^{full MT}$=%5.3f, k=%5.3f' % tuple(popt)

		ax2.plot([min(xcont), max(xcont)], [func(10, *popt), func(10, *popt)], color=COLORS[i])


	ax2.set_ylabel("Bloch T$_1$ / s", fontsize=FS)
	ax2.set_xlabel("T$_{RF}$ / ms", fontsize=FS)

	ax2.tick_params(axis='both', which='major', labelsize=FS-3)
	ax2.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)
	# ax2.set_xlim((VMIN, VMAX))
	# ax2.set_ylim((VMIN, VMAX))
	asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
	ax2.set_aspect(asp)
	ax2.legend(fontsize=FS-7)

	fig.add_subplot(ax2)


	fig.savefig(outfile + ".png", bbox_inches='tight', transparent=False)



	text=r'''\begin{tabular}{c|c|c|c} & $a$ [s] & $b$ [s] & $k'$ [s] \\\hline''' \
		+ '''\n''' \
		+ r''' \textbf{ROI 1} & ''' \
	        + str(np.round(para[0][0],3)) +'$\pm$'+str(ceil(err[0][0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(para[0][1],3)) +'$\pm$'+str(ceil(err[0][1]*1000)/1000 ) \
		+ '''&''' \
	        + str(np.round(para[0][2],3)) +'$\pm$'+str(ceil(err[0][2]*1000)/1000 ) \
	        + r'''\\''' \
		+ '''\n''' \
		+ r''' \textbf{ROI 2} & ''' \
	        + str(np.round(para[1][0],3)) +'$\pm$'+str(ceil(err[1][0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(para[1][1],3)) +'$\pm$'+str(ceil(err[1][1]*1000)/1000 ) \
		+ '''&''' \
	        + str(np.round(para[1][2],3)) +'$\pm$'+str(ceil(err[1][2]*1000)/1000 ) \
	        + r'''\\''' \
		+ '''\n''' \
		+ r''' \textbf{ROI 3} & ''' \
	        + str(np.round(para[2][0],3)) +'$\pm$'+str(ceil(err[2][0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(para[2][1],3)) +'$\pm$'+str(ceil(err[2][1]*1000)/1000 ) \
		+ '''&''' \
	        + str(np.round(para[2][2],3)) +'$\pm$'+str(ceil(err[2][2]*1000)/1000 ) \
	        + r'''\\''' \
		+ '''\n''' \
		+ r''' \textbf{ROI 4} & ''' \
	        + str(np.round(para[3][0],3)) +'$\pm$'+str(ceil(err[3][0]*1000)/1000 ) \
	        + '''&''' \
	        + str(np.round(para[3][1],3)) +'$\pm$'+str(ceil(err[3][1]*1000)/1000 ) \
		+ '''&''' \
	        + str(np.round(para[3][2],3)) +'$\pm$'+str(ceil(err[3][2]*1000)/1000 ) \
	        + r'''\\''' \
		+ '''\n''' \
		+ '''\end{tabular}'''



	if (os.path.isfile("tables.txt")):
		os.remove("tables.txt")

	f = open("tables.txt", "a")
	f.write(text)
	f.close()
