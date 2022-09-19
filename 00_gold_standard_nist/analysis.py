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

from math import ceil


import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

# Global variables

FS=20

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'k', 'w', 'burlywood', 'lightcyan', 'mediumpurple', 'plum', 'slategrey']

DARK = 1 #dark layout?

VMAX = 2.9
VMAX2 = 0.5
VMIN = 0

DIFF_SCALING = 3


BCOLOR='white'  # Background color
TCOLOR='black'  # Text color



def perform_roi_analysis(paramap, roi):

        segment = paramap * roi

        # Set zeros to be invalid for mean calculation
        segment_m = np.ma.masked_equal(segment, 0)

        return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

        #Error if wrong number of parameters
        if( len(sys.argv) < 4):
                print( "Plotting" )
                print( "#-----------------------------------------------" )
                print( "Usage: create_figure.py <T1 map> <T2 map> <outfile> <ROI 1> ... <ROI N>" )
                exit()

        sysargs = sys.argv

        # Load maps
        t1 = np.abs(cfl.readcfl(sysargs[1]).squeeze())
        t1 = t1[:,:,1]  # Extract T1 map
        t1[t1 == np.inf] = 0
        
        t2 = np.abs(cfl.readcfl(sysargs[2]).squeeze())
        t2 = t2[:,:,1]  # Extract T2 map
        t2[t2 == np.inf] = 0


        # Define output filename
        outfile = sysargs[3]

        # Load and stack all passed ROIs
        print("Passed ROIs are:")

        rois = []

        for i in sysargs[4:]:
        
                print("\t", i)

                current_roi = np.abs(cfl.readcfl(i).squeeze())

                rois.append(current_roi)

        # --------------------------------------
        #         Create visualization
        # --------------------------------------

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
        


        fig = plt.figure(num = 1, figsize=(16, 10), dpi=120, edgecolor='w')

        left = gridspec.GridSpec(1, 2, wspace=0.2, hspace=0, figure=fig)

        # --------------------------------------
        #               T1 map
        # --------------------------------------

        ax1 = fig.add_subplot(left[0])

        # Layer with image

        t1_m = np.ma.masked_equal(t1, 0)

        im = ax1.imshow(t1_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Add Layer with ROIs
        for i in range(len(rois)):

                # Single color for ROI
                cmap_roi = colors.ListedColormap(COLORS[i])
                roi_tmp = np.ma.masked_equal(rois[i], 0)
                
                # Plot ROI as overlay
                im = ax1.imshow(roi_tmp, origin='lower', cmap=cmap_roi, alpha=0.6)

                # Add arrow pointing to ROI
                ybase = np.min(np.where(1 == roi_tmp)[0])
                xbase = np.max(np.where(1 == roi_tmp)[1])

                ax1.text(xbase+2, ybase, str(i+1), fontsize=FS+5, fontweight='bold', color=COLORS[i])

        # Recreate Colorbar from image
        im = ax1.imshow(t1_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im, cax=cax)
        cbar.set_label("T$_1$ / s", fontsize=FS)
        cbar.ax.tick_params(labelsize=FS)

        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.xaxis.set_ticks_position('none')
        ax1.yaxis.set_ticks_position('none')

        fig.add_subplot(ax1)

        # # --------------------------------------
        # #              T2 map
        # # --------------------------------------

        ax2 = fig.add_subplot(left[1])

        t2_m = np.ma.masked_equal(t2, 0)

        im2 = ax2.imshow(t2_m, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im2, cax=cax)
        cbar.set_label("T$_2$ / s", fontsize=FS)
        cbar.ax.tick_params(labelsize=FS)

        ax2.set_yticklabels([])
        ax2.set_xticklabels([])
        ax2.xaxis.set_ticks_position('none')
        ax2.yaxis.set_ticks_position('none')
        # ax2.set_axis_off()

        fig.add_subplot(ax2)

        # --------------------------------------
        #           ROI Analysis
        # --------------------------------------

        tube = []
        t1_values = []
        t1_std = []
        t2_values = []
        t2_std = []

        ind = 1
        for i in rois:

                tube.append(ind)

                val, std = perform_roi_analysis(t1, i)
                t1_values.append(val)
                t1_std.append(std)

                val2, std2 = perform_roi_analysis(t2, i)
                t2_values.append(val2)
                t2_std.append(std2)

                ind += 1

        out = np.flip(np.stack((tube, t1_values, t1_std, t2_values, t2_std), axis=1), axis=0)

        np.savetxt(outfile + '.txt', out)

        fig.savefig(outfile + '.png', bbox_inches='tight', transparent=False)
