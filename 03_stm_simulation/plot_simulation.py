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

FS=20
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
        modev = data[:,data[0,:] == 0]
        odev = data[:,data[0,:] == 1]
        finite = data[:,data[0,:] == 2]
        finite2 = data[:,data[0,:] == 3]
        finite3 = data[:,data[0,:] == 4]

        # Convert [rad/ms] to slice thickness [cm]
        distance = np.real(modev[1,:])     # [m]
        distance *= 1000                    # [mm]



        # Import speed data

        speed_data = np.loadtxt(sysargs[3], dtype=complex, unpack=True) #num, tr, speed, x, y, z

        # Split datasets in its individual methods
        speed_modev = speed_data[:,speed_data[0,:] == 0]
        speed_odev = speed_data[:,speed_data[0,:] == 1]
        speed_finite = speed_data[:,speed_data[0,:] == 2]
        speed_finite2 = speed_data[:,speed_data[0,:] == 3]
        speed_finite3 = speed_data[:,speed_data[0,:] == 4] 


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

        fig = plt.figure(num=1, figsize=(30, 14), dpi=120)

        outer = gridspec.GridSpec(1, 3, wspace=0.3, hspace=0, figure=fig)

        left = gridspec.GridSpecFromSubplotSpec(2, 1,
                        subplot_spec=outer[0], wspace=0, hspace=0.2)

        # Main Slice-Profile Visualization

        ax1 = fig.add_subplot(left[0])

        ax1.text(np.min(distance)-3, 1.1, 'A', fontsize=FS+30, fontweight='bold', color=TCOLOR)

        ax1.plot(distance, np.real(odev[2,:]), 'b-', linewidth=LW, label="$M_x$")
        ax1.plot(distance, np.real(odev[3,:]), 'g-', linewidth=LW, label="$M_y$")
        ax1.plot(distance, np.real(odev[4,:]), 'r-', linewidth=LW, label="$M_z$")
        ax1.plot(distance, np.sqrt(odev[2,:]**2+odev[3,:]**2), ':', color=TCOLOR, linewidth=LW, label="|$M_{xy}$|")

        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        plt.locator_params(axis='y', nbins=5)
        ax1.set_xlabel('Position / mm', fontsize=FS)
        ax1.set_ylabel('$\\bf{ODE54}$ Simulation', fontsize=FS)
        ax1.legend(shadow=True, fancybox=True, loc=1, fontsize=FS-5)
        ax1.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)

        # Create subplots for error comparison

        dir = ['x', 'y', 'z']
        color = ['b', 'g', 'r']



        # STM Simulation

        ax12 = fig.add_subplot(left[1])


        # Add text with error factor
        error_factor = np.max(np.abs(modev[2:,:]-odev[2:,:]))

        at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS+5, weight='bold'), frameon=False)
        ax12.add_artist(at)

        for d in range(0,len(dir)):
                ax12.plot(distance, np.abs(modev[2+d,:]-odev[2+d,:])/error_factor, ':', color=color[d], linewidth=LW+0.5, label="$|\epsilon_"+dir[d]+"|$")

        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        ax12.set_xlabel('Position / mm', fontsize=FS)
        ax12.yaxis.get_offset_text().set_fontsize(FS)
        ax12.yaxis.get_offset_text().set_weight('bold')
        ax12.locator_params(axis='y', tight=True, nbins=5)
        ax12.set_ylabel('$\\bf{STM}$ Error $\epsilon$', fontsize=FS)
        ax12.legend(shadow=True, fancybox=True, loc=1, fontsize=FS-5)
        ax12.grid("on", color="black", alpha=.1, linewidth=.5)



        # Discretized Matrix Simulation: Sampling rate fine

        middle = gridspec.GridSpecFromSubplotSpec(3, 1,
                        subplot_spec=outer[1], wspace=0, hspace=0.2)

        ax2 = fig.add_subplot(middle[0])

        # Add text with error factor
        error_factor = np.max(np.abs(finite[2:,:]-odev[2:,:]))

        at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS+5, weight='bold'), frameon=False)
        ax2.add_artist(at)

        for d in range(0,len(dir)):
                ax2.plot(distance, np.abs(finite[2+d,:]-odev[2+d,:])/error_factor, ':', color=color[d], linewidth=LW+0.5, label="$|\epsilon_"+dir[d]+"|$")


        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        # ax2.set_xlabel('Position / mm', fontsize=FS)
        # ax2.set_ylim(0, 5E-3)
        ax2.locator_params(axis='y', nbins=5)
        ax2.yaxis.get_offset_text().set_fontsize(FS)
        ax2.yaxis.get_offset_text().set_weight('bold')
        ax2.set_ylabel('$\\bf{ROT}$ with 0.01 MHz\nError $\epsilon$', fontsize=FS)
        ax2.grid("on", color="black", alpha=.1, linewidth=.5)

        ax2.legend(shadow=True, fancybox=True, loc=1,  fontsize=FS-5)



        ax3 = fig.add_subplot(middle[1])

        # Add text with error factor
        error_factor = np.max(np.abs(finite2[2:,:]-odev[2:,:]))

        at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS+5, weight='bold'), frameon=False)
        ax3.add_artist(at)

        for d in range(0,len(dir)):
                ax3.plot(distance, np.abs(finite2[2+d,:]-odev[2+d,:])/error_factor, ':', color=color[d], linewidth=LW+0.5, label="$|\epsilon_"+dir[d]+"|$")

        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        # ax3.set_xlabel('Position / mm', fontsize=FS)
        # ax3.set_ylim(0, 5E-3)
        ax3.locator_params(axis='y', nbins=5)
        ax3.yaxis.get_offset_text().set_fontsize(FS)
        ax3.yaxis.get_offset_text().set_weight('bold')
        ax3.set_ylabel('$\\bf{ROT}$ with 0.1 MHz\nError $\epsilon$', fontsize=FS)
        ax3.grid("on", color="black", alpha=.1, linewidth=.5)

        ax3.legend(shadow=True, fancybox=True, loc=1,  fontsize=FS-5)



        # Discretized Matrix Simulation: Sampling rate very fine

        ax4 = fig.add_subplot(middle[2])

        # Add text with error factor
        error_factor = np.max(np.abs(finite3[2:,:]-odev[2:,:]))

        at = AnchoredText("x%.0f" % (1/error_factor), loc='upper center', prop=dict(size=FS+5, weight='bold'), frameon=False)
        ax4.add_artist(at)

        for d in range(0,len(dir)):
                ax4.plot(distance, np.abs(finite3[2+d,:]-odev[2+d,:])/error_factor, ':', color=color[d], linewidth=LW+0.5, label="$|\epsilon_"+dir[d]+"|$")

        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        ax4.set_xlabel('Position / mm', fontsize=FS)
        # ax4.set_ylim(0, 5E-3)
        ax4.locator_params(axis='y', nbins=5)
        ax4.yaxis.get_offset_text().set_fontsize(FS)
        ax4.yaxis.get_offset_text().set_weight('bold')
        ax4.set_ylabel('$\\bf{ROT}$ with 1 MHz\nError $\epsilon$', fontsize=FS)
        ax4.grid("on", color="black", alpha=.1, linewidth=.5)

        ax4.legend(shadow=True, fancybox=True, loc=1,  fontsize=FS-5)




        # Plot simulation time

        right = gridspec.GridSpecFromSubplotSpec(3, 1,
                        subplot_spec=outer[2], wspace=0, hspace=0.2)

        ax5 = fig.add_subplot(right[:2])

        ax5.text(-0.25*np.max(np.real(speed_finite3[1,:])), 1.05*np.max(np.real(speed_finite3[2,:])), 'B', fontsize=FS+30, fontweight='bold', color='black')


         # Plot main lines
        ax5.plot(np.real(speed_finite[1,:]), np.real(speed_modev[2,:]), 'r-', linewidth=LW, label="STM")
        ax5.plot(np.real(speed_finite[1,:]), np.real(speed_odev[2,:]), 'g-', linewidth=LW, label="ODE54")
        ax5.plot(np.real(speed_finite[1,:]), np.real(speed_finite[2,:]), 'b-', linewidth=LW, label="ROT with 0.01 MHz")
        ax5.plot(np.real(speed_finite[1,:]), np.real(speed_finite2[2,:]), '-', color='darkorange', linewidth=LW, label="ROT with 0.1 MHz")
        ax5.plot(np.real(speed_finite[1,:]), np.real(speed_finite3[2,:]), '-', color=TCOLOR, linewidth=LW, label="ROT with 1 MHz")


        # Layout stuff...
        ax5.grid("on", color="black", alpha=.5, linewidth=.5)
        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        ax5.set_xlabel('Number of Repetitions', fontsize=FS)
        ax5.set_ylabel('Runtime / s', fontsize=FS)
        ax5.legend(shadow=True, fancybox=True, fontsize=FS-5)


        # Create inset figure 1
        axin1 = inset_axes(ax5, 5, 3 , loc='upper center', bbox_to_anchor=(0.5, -0.15), bbox_transform=ax5.transAxes)

        axin1.plot(np.real(speed_finite[1,:]), np.real(speed_modev[2,:]), 'r-', linewidth=LW, label="STM")
        axin1.plot(np.real(speed_finite[1,:]), np.real(speed_odev[2,:]), 'g-', linewidth=LW, label="ODE54")
        axin1.plot(np.real(speed_finite[1,:]), np.real(speed_finite[2,:]), 'b-', linewidth=LW, label="ROT with 0.01 MHz")
        axin1.plot(np.real(speed_finite[1,:]), np.real(speed_finite2[2,:]), '-', color='darkorange', linewidth=LW, label="ROT with 0.1 MHz")
        axin1.plot(np.real(speed_finite[1,:]), np.real(speed_finite3[2,:]), '-', color=TCOLOR, linewidth=LW, label="ROT with 1 MHz")

        x1, x2, y1, y2 = -10, 150, 0, 1 # specify the limits
        axin1.set_xlim(x1, x2) # apply the x-limits
        axin1.set_ylim(y1, y2) # apply the y-limits
        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        axin1.grid("on", color="black", alpha=.5, linewidth=.5)
        # axin1.set_xlabel('Number of Repetitions', fontsize=FS-5)
        # axin1.set_ylabel('Runtime / s', fontsize=FS-5)
        # plt.xticks(visible=False)
        # plt.yticks(visible=False)

        mark_inset(ax5, axin1, loc1=1, loc2=2, fc="none", ec="0.5")


        # Create inset figure 2
        axin2 = inset_axes(ax5, 5, 3 , loc='center left',  bbox_to_anchor=(1.1, 0.2), bbox_transform=ax5.transAxes)

        axin2.plot(np.real(speed_finite[1,:]), np.real(speed_modev[2,:]), 'r-', linewidth=LW, label="STM")
        axin2.plot(np.real(speed_finite[1,:]), np.real(speed_odev[2,:]), 'g-', linewidth=LW, label="ODE54")
        axin2.plot(np.real(speed_finite[1,:]), np.real(speed_finite[2,:]), 'b-', linewidth=LW, label="ROT with 0.01 MHz")
        axin2.plot(np.real(speed_finite[1,:]), np.real(speed_finite2[2,:]), '-', color='darkorange', linewidth=LW, label="ROT with 0.1 MHz")
        axin2.plot(np.real(speed_finite[1,:]), np.real(speed_finite3[2,:]), '-', color=TCOLOR, linewidth=LW, label="ROT with 1 MHz")

        x1, x2, y1, y2 = 0.81 * np.max(speed_finite[1,:]), 1.01 * np.max(speed_finite[1,:]), 0, 4 # specify the limits
        axin2.set_xlim(x1, x2) # apply the x-limits
        axin2.set_ylim(y1, y2) # apply the y-limits
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

        fig.savefig(filename+".png", bbox_inches='tight', transparent=False)


