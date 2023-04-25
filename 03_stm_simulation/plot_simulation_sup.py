#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 09:37:58 2018

@author: nscho
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

from matplotlib.offsetbox import AnchoredText

FS=22
LW=2

DARK = 0 #dark layout?

GAMMA = 267.513E6   #[rad Hz/T]

GRAD = 12E-3   #[T/m]

BCOLOR='white'  # Background color
TCOLOR='black'  # Text color


if __name__ == "__main__":

	# Error if more than 1 argument
	if (len(sys.argv) < 4):
		print("plot_slice_profile.py: Plot Slice Profile with errors in subplots.")
		print("Usage: python3 plot_slice_profile.py <savename> <file slice-profile [txt]> <file speed [txt]> ")
		exit()

	sysargs = sys.argv

	filename = sysargs[1]

	# Import slice profile data

	data = np.loadtxt(sysargs[2], dtype=complex, unpack=True) #num, moment [1/ms], x, y, z

	# Split datasets in its individual methods
	ode = data[:,data[0,:] == 0]
	# ode1 = data[:,data[0,:] == 1]
	ode2 = data[:,data[0,:] == 2]
	ode3 = data[:,data[0,:] == 3]
	ode4 = data[:,data[0,:] == 4]

	ode_all = [ode, ode2, ode3, ode4]

	stm = data[:,data[0,:] == 5]
	# stm1 = data[:,data[0,:] == 6]
	stm2 = data[:,data[0,:] == 7]
	stm3 = data[:,data[0,:] == 8]
	stm4 = data[:,data[0,:] == 9]

	stm_all = [stm, stm2, stm3, stm4]

	rot = data[:,data[0,:] == 10]
	rot1 = data[:,data[0,:] == 11]
	rot2 = data[:,data[0,:] == 12]
	rot3 = data[:,data[0,:] == 13]
	# rot4 = data[:,data[0,:] == 14]

	rot_all = [rot, rot1, rot2, rot3]

	# Convert [rad/ms] to slice thickness [cm]
	distance = np.real(ode[1,:])     # [m]
	distance *= 1000                    # [mm]



	# Import speed data

	speed_data = np.loadtxt(sysargs[3], dtype=complex, unpack=True) #num, tr, speed, x, y, z

	# Split datasets in its individual methods
	speed_ode = speed_data[:,speed_data[0,:] == 0]
	speed_ode1 = speed_data[:,speed_data[0,:] == 1]
	speed_ode2 = speed_data[:,speed_data[0,:] == 2]
	speed_stm = speed_data[:,speed_data[0,:] == 3]
	speed_stm1 = speed_data[:,speed_data[0,:] == 4]
	speed_stm2 = speed_data[:,speed_data[0,:] == 5]
	speed_rot = speed_data[:,speed_data[0,:] == 6]
	speed_rot1 = speed_data[:,speed_data[0,:] == 7]
	speed_rot2 = speed_data[:,speed_data[0,:] == 8] 


	"""
	------------------------------------
	---------- Visualization -----------
	------------------------------------
	"""

	if "DARK_LAYOUT" in os.environ:
		DARK = int(os.environ["DARK_LAYOUT"])

	if(DARK):
		plt.style.use(['dark_background'])
		BCOLOR='black'
		TCOLOR='white'
	else:
		plt.style.use(['default'])

	fig = plt.figure(num=1, figsize=(50, 14), dpi=120)

	outer = gridspec.GridSpec(1, 4, wspace=0.15, hspace=0, figure=fig)

	left = gridspec.GridSpecFromSubplotSpec(2, 1,
			subplot_spec=outer[0], wspace=0, hspace=0.2)

	# Main Slice-Profile Visualization

	ax1 = fig.add_subplot(left[:])

	ax1.text(np.min(distance)-3, 1.1, 'B', fontsize=FS+30, fontweight='bold', color=TCOLOR)

	ax1.plot(distance, np.real(ode[2,:]), 'b-', linewidth=LW, label="$M_x$")
	ax1.plot(distance, np.real(ode[3,:]), 'g-', linewidth=LW, label="$M_y$")
	ax1.plot(distance, np.real(ode[4,:]), 'r-', linewidth=LW, label="$M_z$")
	ax1.plot(distance, np.sqrt(ode[2,:]**2+ode[3,:]**2), ':', color=TCOLOR, linewidth=LW, label="|$M_{xy}$|")

	plt.xticks(fontsize=FS)
	plt.yticks(fontsize=FS)
	plt.locator_params(axis='y', nbins=5)
	ax1.set_xlabel('Position / mm', fontsize=FS+10)
	ax1.set_title('$\\bf{RK54}$ Reference Simulation', fontsize=FS+10)
	ax1.legend(shadow=True, fancybox=True, loc=1, fontsize=FS)
	ax1.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)

	# Create subplots for error comparison

	dir = ['x', 'y', 'z']
	color = ['b', 'g', 'r']


	# 		ODE

	tol = ['1E-6', '1E-4', 'tol=1E-3', '1E-2']

	middle = gridspec.GridSpecFromSubplotSpec(len(stm_all), 1,
			subplot_spec=outer[1], wspace=0, hspace=0.05)

	for i in range(0, len(stm_all)):	

		ax2 = fig.add_subplot(middle[i])

		# Add text with error factor
		error_factor = np.max(np.abs(ode_all[0][2:,:]-ode_all[i][2:,:]))

		if (0 == error_factor):
			error_factor = 1
			ax2.set_ylim(-0.05, 1.05)
		else:
			if (2 == i):
				at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS+15, weight='bold'), frameon=False)
			else:
				at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS, weight='bold', color='gray'), frameon=False)
			
			ax2.add_artist(at)

		for d in range(0,len(dir)):
			ax2.plot(distance, np.abs(ode_all[i][2+d,:]-ode_all[0][2+d,:])/error_factor, ':', color=color[d], linewidth=LW+0.5, label="$|\epsilon_"+dir[d]+"|$")


		plt.xticks(fontsize=FS)
		plt.yticks(fontsize=FS)
		plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
		# ax2.set_xlabel('Position / mm', fontsize=FS)
		# 
		ax2.locator_params(axis='y', nbins=3)
		ax2.yaxis.get_offset_text().set_fontsize(FS)
		ax2.yaxis.get_offset_text().set_weight('bold')
		# ax2.set_ylabel(tol[i], fontsize=FS)
		ax2.grid("on", color="black", alpha=.1, linewidth=.5)

		if (2 == i):
			at2 = AnchoredText(tol[i], loc='upper left', prop=dict(size=FS+5, weight='bold', color=TCOLOR), frameon=True)
		else:
			at2 = AnchoredText(tol[i], loc='upper left', prop=dict(size=FS-5, weight='bold', color='gray'), frameon=True)
		at2.patch.set_boxstyle("round,pad=0.,rounding_size=0.4")
		ax2.add_artist(at2)

		if (0 == i):
			ax2.set_title('Point-wise Error: $\\bf{RK54}$', fontsize=FS+10)
			ax2.legend(shadow=True, fancybox=True, loc=1,  fontsize=FS)

		if (len(ode_all)-1 == i):
			ax2.set_xlabel('Position / mm', fontsize=FS+10)

		if (len(ode_all)-1 != i):
			ax2.set_xticklabels([])
			# ax2.set_yticklabels([])



	#		STM

	middle2 = gridspec.GridSpecFromSubplotSpec(len(stm_all), 1,
			subplot_spec=outer[2], wspace=0, hspace=0.05)

	for i in range(0, len(stm_all)):	

		ax3 = fig.add_subplot(middle2[i])

		# Add text with error factor
		error_factor = np.max(np.abs(ode_all[0][2:,:]-stm_all[i][2:,:]))

		if (0 == error_factor):
			error_factor = 1
			ax3.set_ylim(-0.05, 1.05)
		else:
			if (2 == i):
				at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS+15, weight='bold'), frameon=False)
			else:
				at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS, weight='bold', color='gray'), frameon=False)

			ax3.add_artist(at)

		for d in range(0,len(dir)):
			ax3.plot(distance, np.abs(stm_all[i][2+d,:]-ode_all[0][2+d,:])/error_factor, ':', color=color[d], linewidth=LW+0.5, label="$|\epsilon_"+dir[d]+"|$")


		plt.xticks(fontsize=FS)
		plt.yticks(fontsize=FS)
		plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
		# ax3.set_xlabel('Position / mm', fontsize=FS)
		# 
		ax3.locator_params(axis='y', nbins=3)
		ax3.yaxis.get_offset_text().set_fontsize(FS)
		ax3.yaxis.get_offset_text().set_weight('bold')
		# ax3.set_ylabel(tol[i], fontsize=FS)
		ax3.grid("on", color="black", alpha=.1, linewidth=.5)

		if (2 == i):
			at2 = AnchoredText(tol[i], loc='upper left', prop=dict(size=FS+5, weight='bold', color=TCOLOR), frameon=True)
		else:
			at2 = AnchoredText(tol[i], loc='upper left', prop=dict(size=FS-5, weight='bold', color='gray'), frameon=True)
		at2.patch.set_boxstyle("round,pad=0.,rounding_size=0.4")
		ax3.add_artist(at2)

		if (0 == i):
			ax3.set_title('PWE: $\\bf{STM}$', fontsize=FS+10)
			# ax3.legend(shadow=True, fancybox=True, loc=1,  fontsize=FS-5)

		if (len(ode_all)-1 == i):
			ax3.set_xlabel('Position / mm', fontsize=FS+10)

		ax3.set_yticklabels([])

		if (len(ode_all)-1 != i):
			ax3.set_xticklabels([])


	#		ROT

	sr = ['100 MHz', '10 MHz', 'SR=1 MHz', '0.1 MHz']

	middle2 = gridspec.GridSpecFromSubplotSpec(len(stm_all), 1,
			subplot_spec=outer[3], wspace=0, hspace=0.05)

	for i in range(0, len(stm_all)):	

		ax4 = fig.add_subplot(middle2[i])

		# Add text with error factor
		error_factor = np.max(np.abs(ode_all[0][2:,:]-rot_all[i][2:,:]))

		if (0 == error_factor):
			error_factor = 1
			ax4.set_ylim(-0.05, 1.05)
		else:
			if (2 == i):
				at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS+15, weight='bold'), frameon=False)
			else:
				at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS, weight='bold', color='gray'), frameon=False)

			ax4.add_artist(at)

		for d in range(0,len(dir)):
			ax4.plot(distance, np.abs(rot_all[i][2+d,:]-ode_all[0][2+d,:])/error_factor, ':', color=color[d], linewidth=LW+0.5, label="$|\epsilon_"+dir[d]+"|$")


		plt.xticks(fontsize=FS)
		plt.yticks(fontsize=FS)
		plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
		# ax4.set_xlabel('Position / mm', fontsize=FS)
		# 
		ax4.locator_params(axis='y', nbins=3)
		ax4.yaxis.get_offset_text().set_fontsize(FS)
		ax4.yaxis.get_offset_text().set_weight('bold')
		# ax4.set_ylabel(sr[i]+' Hz', fontsize=FS)
		ax4.grid("on", color="black", alpha=.1, linewidth=.5)

		if (2 == i):
			at2 = AnchoredText(sr[i], loc='upper left', prop=dict(size=FS+5, weight='bold', color=TCOLOR), frameon=True)
		else:
			at2 = AnchoredText(sr[i], loc='upper left', prop=dict(size=FS-5, weight='bold', color='gray'), frameon=True)

		at2.patch.set_boxstyle("round,pad=0.,rounding_size=0.4")
		ax4.add_artist(at2)

		if (0 == i):
			ax4.set_title('PWE: $\\bf{ROT}$', fontsize=FS+10)
			# ax4.legend(shadow=True, fancybox=True, loc=1,  fontsize=FS-5)

		if (len(ode_all)-1 == i):
			ax4.set_xlabel('Position / mm', fontsize=FS+10)

		ax4.set_yticklabels([])

		if (len(ode_all)-1 != i):
			ax4.set_xticklabels([])

	fig.savefig(filename+"_B.png", bbox_inches='tight', transparent=False)





	# Plot simulation time


	fig2 = plt.figure(num=2, figsize=(8, 8), dpi=120)

	

	ax5 = fig2.add_subplot(111)

	ax5.text(-0.35*np.max(np.real(speed_rot[1,:])), 1.1*np.max(np.real(speed_rot[2,:])), 'C', fontsize=FS+25, fontweight='bold', color='black')


	# Plot main lines
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_stm[2,:]), 'r-', linewidth=LW, label="STM, tol=1E-6")
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_stm1[2,:]), 'r--', linewidth=LW, label="STM, tol=1E-5")
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_stm2[2,:]), 'r:', linewidth=LW, label="STM, tol=1E-4")
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_ode[2,:]), 'g-', linewidth=LW, label="RK54, tol=1E-6")
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_ode1[2,:]), 'g--', linewidth=LW, label="RK54, tol=1E-5")
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_ode2[2,:]), 'g:', linewidth=LW, label="RK54, tol=1E-4")
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_rot[2,:]), 'b-', linewidth=LW, label="ROT with 10 MHz")
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_rot1[2,:]), 'b--', linewidth=LW, label="ROT with 1 MHz")
	ax5.plot(np.real(speed_rot[1,:]), np.real(speed_rot2[2,:]), 'b:', linewidth=LW, label="ROT with 0.1 MHz")


	# Layout stuff...
	ax5.locator_params(axis='y', nbins=5)
	ax5.grid("on", color="black", alpha=.5, linewidth=.5)
	plt.xticks(fontsize=FS)
	plt.yticks(fontsize=FS)
	ax5.set_xlabel('Number of Repetitions', fontsize=FS)
	ax5.set_ylabel('Runtime / s', fontsize=FS)
	ax5.legend(shadow=True, fancybox=True, fontsize=FS-5,loc='lower left', bbox_to_anchor=(1.2, 0.44))


	# Create inset figure 1
	axin1 = inset_axes(ax5, 7, 2 , loc='upper center', bbox_to_anchor=(0.5, -0.15), bbox_transform=ax5.transAxes)

	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_stm[2,:]), 'r-', linewidth=LW, label="STM, tol=1E-6")
	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_stm1[2,:]), 'r--', linewidth=LW, label="STM, tol=1E-5")
	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_stm2[2,:]), 'r:', linewidth=LW, label="STM, tol=1E-4")
	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_ode[2,:]), 'g-', linewidth=LW, label="RK54, tol=1E-6")
	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_ode1[2,:]), 'g--', linewidth=LW, label="RK54, tol=1E-5")
	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_ode2[2,:]), 'g:', linewidth=LW, label="RK54, tol=1E-4")
	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_rot[2,:]), 'b-', linewidth=LW, label="ROT with 10 MHz")
	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_rot1[2,:]), 'b--', linewidth=LW, label="ROT with 1 MHz")
	axin1.plot(np.real(speed_rot[1,:]), np.real(speed_rot2[2,:]), 'b:', linewidth=LW, label="ROT with 0.1 MHz")

	x1, x2, y1, y2 = -10, 150, 0, 1 # specify the limits
	axin1.set_xlim(x1, x2) # apply the x-limits
	axin1.set_ylim(y1, y2) # apply the y-limits
	axin1.locator_params(axis='y', nbins=3)
	axin1.locator_params(axis='x', nbins=7)
	plt.xticks(fontsize=FS)
	plt.yticks(fontsize=FS)
	axin1.grid("on", color="black", alpha=.5, linewidth=.5)
	# axin1.set_xlabel('Number of Repetitions', fontsize=FS-5)
	# axin1.set_ylabel('Runtime / s', fontsize=FS-5)
	# plt.xticks(visible=False)
	# plt.yticks(visible=False)

	mark_inset(ax5, axin1, loc1=1, loc2=2, fc="none", ec="0.5")


	# Create inset figure 2
	axin2 = inset_axes(ax5, 4, 2 , loc='center left',  bbox_to_anchor=(1.1, 0.2), bbox_transform=ax5.transAxes)

	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_stm[2,:]), 'r-', linewidth=LW, label="STM, tol=1E6")
	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_stm1[2,:]), 'r--', linewidth=LW, label="STM, tol=1E5")
	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_stm2[2,:]), 'r:', linewidth=LW, label="STM, tol=1E4")
	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_ode[2,:]), 'g-', linewidth=LW, label="RK54, tol=1E6")
	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_ode1[2,:]), 'g--', linewidth=LW, label="RK54, tol=1E5")
	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_ode2[2,:]), 'g:', linewidth=LW, label="RK54, tol=1E4")
	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_rot[2,:]), 'b-', linewidth=LW, label="ROT with 10 MHz")
	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_rot1[2,:]), 'b--', linewidth=LW, label="ROT with 1 MHz")
	axin2.plot(np.real(speed_rot[1,:]), np.real(speed_rot2[2,:]), 'b:', linewidth=LW, label="ROT with 0.1 MHz")

	x1, x2, y1, y2 = 0.81 * np.max(speed_rot[1,:]), 1.01 * np.max(speed_rot[1,:]), 0, 4 # specify the limits
	axin2.set_xlim(x1, x2) # apply the x-limits
	axin2.set_ylim(y1, y2) # apply the y-limits
	axin2.locator_params(axis='y', nbins=3)
	axin2.locator_params(axis='x', nbins=5)
	plt.xticks(fontsize=FS)
	plt.yticks(fontsize=FS)
	axin2.grid("on", color="black", alpha=.5, linewidth=.5)
	# axin2.set_xlabel('Number of Repetitions', fontsize=FS-5)
	# axin2.set_ylabel('Runtime / s', fontsize=FS-5)
	# plt.xticks(visible=False)
	# plt.yticks(visible=False)

	mark_inset(ax5, axin2, loc1=2, loc2=3, fc="none", ec="0.5")


	# plt.tight_layout(pad=5)
	# plt.show(block = True)

	fig2.savefig(filename+"_C.png", bbox_inches='tight', transparent=False)


	


