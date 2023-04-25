#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
						mark_inset)

import imutils

import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

# Global variables

FS=20
MS=11

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'peru', 'palegreen', 'slategray', 'pink', 'springgreen', 'slateblue', 'maroon']

WBC = ['white']

DARK = 0

# Define max values
VMAXT1 = 3.1
VMAXT2 = 1.1

VMIN = 0


BCOLOR='white'  # Background color
TCOLOR='black'  # Text color

# Correction of phantom acquisition
ANGLE = -28

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
		print( "Usage: create_figure.py <refvalues [txt]> <Bloch T1 map> <Bloch T2 map> <outfile> <ROI 1> ... <ROI N>" )
		exit()

	sysargs = sys.argv

	# Load reference data
	ref_num, reft1, stdt1, reft2, stdt2 = np.loadtxt(sysargs[1]+'.txt', unpack=True)

	# Load Bloch T1 reco
	bloch_t1 = np.abs(cfl.readcfl(sysargs[2]).squeeze())
	bloch_t1[bloch_t1 == np.inf] = 0

	# Load Bloch T2 reco
	bloch_t2 = np.abs(cfl.readcfl(sysargs[3]).squeeze())
	bloch_t2[bloch_t2 == np.inf] = 0

	# Define output filename
	outfile = sysargs[4]

	# Load and stack all passed ROIs
	print("Passed ROIs are:")

	rois = []

	for i in sysargs[5:]:

		print("\t", i)

		current_roi = np.abs(cfl.readcfl(i).squeeze())

		rois.append(current_roi)


	# --------------------------------------
	#           ROI Analysis
	# --------------------------------------

	t1 = []
	t1_std = []
	t2 = []
	t2_std = []

	# Iterate over experiments
	for e in range(0, np.shape(bloch_t1)[2]):

		t1_data = bloch_t1[:,:,e]
		t2_data = bloch_t2[:,:,e]


		bloch_values_t1 = []
		bloch_std_t1 = []
		bloch_values_t2 = []
		bloch_std_t2 = []

		# Iterate over ROIs
		for i in rois:

			bval, bstd = perform_roi_analysis(t1_data, i)
			bloch_values_t1.append(bval)
			bloch_std_t1.append(bstd)

			bval, bstd = perform_roi_analysis(t2_data, i)
			bloch_values_t2.append(bval)
			bloch_std_t2.append(bstd)

		t1.append(bloch_values_t1)
		t1_std.append(bloch_std_t1)

		t2.append(bloch_values_t2)
		t2_std.append(bloch_std_t2)

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

	fig = plt.figure(num = 1, figsize=(32, 10), dpi=120)

	outer = gridspec.GridSpec(1, 2, wspace=-0.2, hspace=0)

	left = gridspec.GridSpecFromSubplotSpec(2, 1,
			subplot_spec=outer[0], wspace=0, hspace=0.3)

	# --------------------------------------
	#          Bloch T1 map
	# --------------------------------------

	ax1 = plt.Subplot(fig, left[0])

	# Layer with image

	bloch_rot = imutils.rotate(bloch_t1[:,:,0], angle=ANGLE)

	bloch_t1_m = np.ma.masked_equal(bloch_rot, 0)     # Take HypSec with SP reco

	im = ax1.imshow(bloch_t1_m, origin='lower', cmap=my_cmap, vmax=VMAXT1, vmin=VMIN)

	# Add Layer with ROIs
	for i in range(len(rois)):

		# Single color for ROI
		cmap_roi = colors.ListedColormap(WBC)

		roi_rot = imutils.rotate(rois[i], angle=ANGLE)

		roi_tmp = np.ma.masked_equal(roi_rot, 0)

		# Plot ROI as overlay
		im = ax1.imshow(roi_tmp, origin='lower', cmap=cmap_roi, alpha=0.6)

		# Add arrow pointing to ROI
		ybase = np.max(np.where(1 == roi_tmp)[0])
		xbase = np.max(np.where(1 == roi_tmp)[1])
		ax1.text(xbase, ybase+1, str(i+1), fontsize=FS, fontweight='bold', color=TCOLOR)

	# Recreate Colorbar from image
	im = ax1.imshow(bloch_t1_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAXT1, vmin=VMIN)

	# Small legend indicating ROIs
	ax1.text(0.25*np.shape(roi_tmp)[0], 0.1*np.shape(roi_tmp)[1], '\u2B24 ROIs',
		fontsize=FS+4, fontweight='bold', color='white',
		ha="center", va="center",
		bbox=dict(boxstyle="round", color="gray", alpha=0.5)
	)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	# cbar.set_label("$\\bf{T}_1$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS+5)
	# cax.set_visible(False)

	ax1.set_yticklabels([])
	ax1.set_xticklabels([])
	ax1.xaxis.set_ticks_position('none')
	ax1.yaxis.set_ticks_position('none')
	ax1.tick_params(axis='x', colors='white')
	# ax1.set_axis_off()
	# ax1.set_title("$\\bf{Simulated~Phantom}$", fontsize=FS+5)

	ax1.text(-0.1*np.shape(roi_tmp)[0], 0.5*np.shape(roi_tmp)[0], 'Bloch T$_1$ / s',
		fontsize=FS+10, fontweight='bold', color=TCOLOR,
		ha="center", va="center", rotation=90,
	)

	for axis in ['top','bottom','left','right']:
		ax1.spines[axis].set_linewidth(2)

	# Figure label "A"
	ax1.text(-0.3*np.shape(bloch_t1_m)[0], 1.1*np.shape(bloch_t1_m)[0], 'B', fontsize=FS+14, fontweight='bold', color=TCOLOR)
	ax1.text(-0.15*np.shape(bloch_t1_m)[0], 1.1*np.shape(bloch_t1_m)[0], "$\\bf{Measured~Data}$", fontsize=FS+2, fontweight='bold', color=TCOLOR)


	fig.add_subplot(ax1)

	# --------------------------------------
	#          Bloch T2 map
	# --------------------------------------

	ax2 = plt.Subplot(fig, left[1])

	my_cmap2 = copy.copy(cm.get_cmap('turbo'))
	my_cmap2.set_bad(BCOLOR)

	bloch2_rot = imutils.rotate(bloch_t2[:,:,0], angle=ANGLE)

	bloch_t2_m = np.ma.masked_equal(bloch2_rot, 0)     # Take HypSec with SP reco

	im = ax2.imshow(bloch_t2_m, origin='lower', cmap=my_cmap2, vmax=VMAXT2, vmin=VMIN)

	# Ensure same scaling as map with colorbar has
	divider = make_axes_locatable(ax2)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(im, cax=cax)
	# cbar.set_label("$\\bf{T}_2$ / s", fontsize=FS)
	cbar.ax.tick_params(labelsize=FS+5)
	# cax.set_visible(False)

	ax2.set_yticklabels([])
	ax2.set_xticklabels([])
	ax2.xaxis.set_ticks_position('none')
	ax2.yaxis.set_ticks_position('none')
	# ax2.set_axis_off()

	ax2.text(-0.1*np.shape(roi_tmp)[0], 0.5*np.shape(roi_tmp)[0], 'Bloch T$_2$ / s',
		fontsize=FS+10, fontweight='bold', color=TCOLOR,
		ha="center", va="center", rotation=90,
	)

	for axis in ['top','bottom','left','right']:
		ax2.spines[axis].set_linewidth(2)

	fig.add_subplot(ax2)


	ind_list = [1, 2, 0]

	right = gridspec.GridSpecFromSubplotSpec(2, 3,
			subplot_spec=outer[1], wspace=0.4, hspace=0.3)

	for d in range(0, 3):

		# --------------------------------------
		#        Bland-Altman T1
		# --------------------------------------

		ax3 = plt.Subplot(fig, right[d])

		ind = ind_list[d]

		# Calculate mean and diff for Bland-Altman Plot

		removed_values_t1 = 0

		data_ref = np.asarray(reft1[removed_values_t1:])
		data_meas = np.asarray(t1[ind][removed_values_t1:])

		mean = np.mean([data_ref, data_meas], axis=0)
		diff = data_ref - data_meas

		md = np.mean(diff)
		sd = np.std(diff, axis=0)

		for i in range(0, np.shape(data_ref)[0]):

			ax3.scatter(mean[i], diff[i], marker='*', s=400, color=COLORS[i-1+removed_values_t1], label='ROI: '+str(i))

			if (1 == d):
				ax3.text(mean[i], 0.01+diff[i], str(i+1), fontsize=FS, fontweight='bold', color=COLORS[i-1+removed_values_t1])

		ax3.axhline(md, color=TCOLOR, linestyle='--', linewidth = 4)
		ax3.axhline(md + 1.96*sd, color='gray', linestyle='--', linewidth = 4)
		ax3.axhline(md - 1.96*sd, color='gray', linestyle='--', linewidth = 4)

		# ax3.set_title("$\\bf{Perfect~Inversion}$", fontsize=FS+2, pad=10)

		ax3.tick_params(labelsize=FS+3)
		ax3.set_ylim((-0.15, 0.2))
		ax3.set_xlim((0, 3))
		asp = np.diff(ax3.get_xlim())[0] / np.diff(ax3.get_ylim())[0] * 0.9 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
		ax3.set_aspect(asp)
		ax3.grid(alpha=0.2)

		for axis in ['top','bottom','left','right']:
			ax3.spines[axis].set_linewidth(2)
		ax3.tick_params(width=2)

		if (0 == d):
			# ax3.legend()
			ax3.set_title("$\\bf{Perfect~Inversion}$", fontsize=FS+5, pad=20)
			ax3.set_ylabel("($\\bf{Ref-Meas.}$)", fontsize=FS+5)
		if (1 == d):
			ax3.set_title("$\\bf{Slice}$", fontsize=FS+5, pad=20)
			# ax3.set_yticklabels([])
			ax3.set_xlabel("$\\bf{Mean}$ T$_1$ / s", fontsize=FS+3)
		if (2 == d):
			ax3.set_title("$\\bf{Pulse~+~Slice}$", fontsize=FS+5, pad=20)
			ax3.set_yticklabels([])
			ax3.text(0.7*np.max(mean), +0.01, 'mean', color=TCOLOR, fontsize=FS)
			ax3.text(0.7*np.max(mean), 1.1*(md+1.96*sd), '1.96$\sigma$', color='gray', fontsize=FS)
			ax3.text(0.7*np.max(mean), 0.9*(md-1.96*sd), '-1.96$\sigma$', color='gray', fontsize=FS)

		fig.add_subplot(ax3)



		# --------------------------------------
		#        Bland-Altman T2
		# --------------------------------------

		ax4 = plt.Subplot(fig, right[d+3])

		ind = ind_list[d]

		# Calculate mean and diff for Bland-Altman Plot

		data_ref = np.asarray(reft2)
		data_meas = np.asarray(t2[ind])

		print(data_ref)
		print(data_meas)

		mean = np.mean([data_ref, data_meas], axis=0)
		diff = data_ref - data_meas

		md = np.mean(diff)
		sd = np.std(diff, axis=0)

		for i in range(0, np.shape(data_ref)[0]):

			ax4.scatter(mean[i], diff[i], marker='*', s=400, color=COLORS[i-1], label='ROI: '+str(i))

			# if (0 == d):
			#         ax4.text(mean[i], diff[i], str(i+removed_values_t2), fontsize=FS-5, fontweight='bold', color=COLORS[i-1+removed_values_t2])

		ax4.axhline(md, color=TCOLOR, linestyle='--', linewidth = 4)
		ax4.axhline(md + 1.96*sd, color='gray', linestyle='--', linewidth = 4)
		ax4.axhline(md - 1.96*sd, color='gray', linestyle='--', linewidth = 4)

		# ax4.set_title("$\\bf{Perfect~Inversion}$", fontsize=FS+2, pad=10)

		ax4.tick_params(labelsize=FS+3)
		# ax4.set_ylim((-0.08, 0.05))
		# ax4.set_xlim((0, 0.5))
		asp = np.diff(ax4.get_xlim())[0] / np.diff(ax4.get_ylim())[0] * 0.9 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
		ax4.set_aspect(asp)
		ax4.grid(alpha=0.2)

		for axis in ['top','bottom','left','right']:
			ax4.spines[axis].set_linewidth(2)
		ax4.tick_params(width=2)

		if (0 == d):
			# ax4.legend()
			ax4.set_ylabel("($\\bf{Ref-Meas.}$)", fontsize=FS+5)
		if (1 == d):
			ax4.set_xlabel("$\\bf{Mean}$ T$_2$ / s", fontsize=FS+3)
			ax4.text(0.7*np.max(mean), -0.005, 'mean', color=TCOLOR, fontsize=FS)
			ax4.text(0.7*np.max(mean), 0.6*(md+1.96*sd), '1.96$\sigma$', color='gray', fontsize=FS)
			ax4.text(0.7*np.max(mean), 0.92*(md-1.96*sd), '-1.96$\sigma$', color='gray', fontsize=FS)

		fig.add_subplot(ax4)
	
	# plt.tight_layout()
	
	fig.savefig(outfile + ".png", bbox_inches='tight', transparent=False)
