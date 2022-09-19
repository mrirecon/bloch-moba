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
        if( len(sys.argv) == 4):
                print( "Plotting" )
                print( "#-----------------------------------------------" )
                print( "Usage: create_figure.py <LL T1 map> <Bloch T1 map> <ROIS> <outfile>" )
                exit()

        sysargs = sys.argv

        # Load maps
        ll_map = np.abs(cfl.readcfl(sysargs[1]).squeeze())
        ll_map[ll_map == np.inf] = 0
        
        bloch_map = np.abs(cfl.readcfl(sysargs[2]).squeeze())
        bloch_map[bloch_map == np.inf] = 0

        rois = np.abs(cfl.readcfl(sysargs[3]).squeeze())
        rois[rois == np.inf] = 0

        # Define output filename
        outfile = sysargs[4]

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


        fig = plt.figure(num = 1, figsize=(30, 5), dpi=120, edgecolor='w')

        outer = gridspec.GridSpec(1, 2, wspace=-0.17, hspace=0)

        left = gridspec.GridSpecFromSubplotSpec(1, 3,
                        subplot_spec=outer[0], wspace=-0, hspace=0)

        # --------------------------------------
        #          Look-Locker T1 map
        # --------------------------------------

        ax1 = plt.Subplot(fig, left[0])

        # Layer with image

        ll_map_m = np.ma.masked_equal(ll_map, 0)

        im = ax1.imshow(ll_map_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Add Layer with ROIs
        # First and last ROIs are not interesting because they are filled with water
        for i in range(1, np.shape(rois)[2]-1):

                # Single color for ROI
                cmap_roi = colors.ListedColormap(COLORS[i-1])
                roi_tmp = np.ma.masked_equal(rois[:,:,i], 0)
                
                # Plot ROI as overlay
                im = ax1.imshow(roi_tmp, origin='lower', cmap=cmap_roi, alpha=0.6)

                # Add arrow pointing to ROI
                ybase = np.max(np.where(1 == roi_tmp)[0])
                xbase = np.max(np.where(1 == roi_tmp)[1])
                ax1.arrow(xbase+20, ybase+20, -12, -12, head_width=5, color=COLORS[i-1])

        # Recreate Colorbar from image
        im = ax1.imshow(ll_map_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cax.set_visible(False)

        ax1.set_title("Look-Locker", fontsize=FS)

        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.xaxis.set_ticks_position('none')
        ax1.yaxis.set_ticks_position('none')

        # Figure label "A"
        ax1.text(-0.3*np.shape(ll_map_m)[0], 1.2*np.shape(ll_map_m)[0], 'A', fontsize=FS+10, fontweight='bold', color=TCOLOR)
        ax1.text(-0.15*np.shape(ll_map_m)[0], 1.2*np.shape(ll_map_m)[0], "$\\bf{Simulated~Data}$", fontsize=FS+2, fontweight='bold', color=TCOLOR)

        fig.add_subplot(ax1)

        # --------------------------------------
        #           Bloch T1 map
        # --------------------------------------

        ax2 = plt.Subplot(fig, left[1])

        bloch_map_m = np.ma.masked_equal(bloch_map, 0)

        im2 = ax2.imshow(bloch_map_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cax.set_visible(False)

        ax2.set_title("Bloch", fontsize=FS)

        ax2.set_yticklabels([])
        ax2.set_xticklabels([])
        ax2.xaxis.set_ticks_position('none')
        ax2.yaxis.set_ticks_position('none')

        fig.add_subplot(ax2)

        # --------------------------------------
        # Difference between Look-Locker and Bloch T1 map
        # --------------------------------------

        ax3 = plt.Subplot(fig, left[2])

        diff_map = np.abs(ll_map - bloch_map)

        diff_map_m = np.ma.masked_equal(diff_map, 0)

        im3 = ax3.imshow(diff_map_m*DIFF_SCALING, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Add scaling as text to Diff image
        ax3.text(0.01*np.shape(diff_map)[0], 0.01*np.shape(diff_map)[0], 'x'+str(DIFF_SCALING), fontsize=FS+20, color=TCOLOR)

        divider = make_axes_locatable(ax3)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im3, cax=cax)
        cbar.set_label("T$_1$ / s", fontsize=FS)
        cbar.ax.tick_params(labelsize=FS)

        ax3.set_title("Difference", fontsize=FS)

        ax3.set_yticklabels([])
        ax3.set_xticklabels([])
        ax3.xaxis.set_ticks_position('none')
        ax3.yaxis.set_ticks_position('none')
        ax3.grid('off')

        fig.add_subplot(ax3)

        # --------------------------------------
        #           ROI Analysis
        # --------------------------------------

        ll_values = []
        ll_std = []
        bloch_values = []
        bloch_std = []

        for i in range(0, np.shape(rois)[2]):

                tmp_roi = rois[:,:,i]

                lval, lstd = perform_roi_analysis(ll_map, tmp_roi)
                ll_values.append(lval)
                ll_std.append(lstd)

                bval, bstd = perform_roi_analysis(bloch_map, tmp_roi)
                bloch_values.append(bval)
                bloch_std.append(bstd)

        # --------------------------------------
        #        ROI Analysis Plot
        # --------------------------------------

        right = gridspec.GridSpecFromSubplotSpec(1, 1,
                        subplot_spec=outer[1], wspace=0, hspace=0)
        
        ax4 = plt.Subplot(fig, right[0])
        plt.grid(color='0.15')

        ax4.set_ylim([0, 1.1*max(ll_values)])

        for i in range(1,len(ll_values)-1):
                ax4.errorbar(ll_values[i], bloch_values[i], xerr=ll_std[i], yerr=bloch_std[i], fmt='*', color=COLORS[i-1], label='ROI '+str(i))

        ax4.plot([VMIN, VMAX], [VMIN, VMAX], ':', color='gray')

        ulim = np.max([max(ll_values), max(bloch_values)])

        ax4.set_ylabel("Bloch T$_1$ / s", fontsize=FS)
        ax4.set_xlabel("Look-Locker T$_1$ / s", fontsize=FS)
        
        ax4.tick_params(axis='both', which='major', labelsize=FS-3)
        ax4.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)
        ax4.set_xlim((VMIN, VMAX))
        ax4.set_ylim((VMIN, VMAX))
        asp = np.diff(ax4.get_xlim())[0] / np.diff(ax4.get_ylim())[0]
        ax4.set_aspect(asp)
        ax4.legend(fontsize=FS-5)

        fig.add_subplot(ax4)
        
        fig.savefig(outfile + ".png", bbox_inches='tight', transparent=False)
