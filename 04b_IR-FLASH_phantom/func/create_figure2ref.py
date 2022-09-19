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

FS=12

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'k', 'w']

DARK = 0

VMAX = 2
VMIN = 0

DIFF_SCALING = 40



def perform_roi_analysis(paramap, roi):

    segment = paramap * roi

    # Set zeros to be invalid for mean calculation
    segment_m = np.ma.masked_equal(segment, 0)

    return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

    if( len(sys.argv) < 5):
        print( "Plotting" )
        print( "#-----------------------------------------------" )
        print( "Usage: create_figure.py <refvalues [txt]> <Bloch T1 map> <outfile> <ROI 1> ... <ROI N>" )
        exit()

    sysargs = sys.argv

    # Load reference data
    ref_num, reft1, stdt1 = np.loadtxt(sysargs[1]+'.txt', unpack=True)
    
    # Load Bloch reco
    bloch_map = np.abs(cfl.readcfl(sysargs[2]).squeeze())
    bloch_map[bloch_map == np.inf] = 0

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

    if "DARK_LAYOUT" in os.environ:
                DARK = int(os.environ["DARK_LAYOUT"])

    if(DARK):
        plt.style.use(['dark_background'])
    else:
        plt.style.use(['default'])

    my_cmap = copy.copy(cm.get_cmap('viridis'))

    if(DARK):
        my_cmap.set_bad('black')
    else:
        my_cmap.set_bad('white')
    


    fig = plt.figure(num = 1, figsize=(24, 5), dpi=120, edgecolor='w')

    outer = gridspec.GridSpec(1, 2, wspace=-0.55, hspace=0)

    left = gridspec.GridSpecFromSubplotSpec(1, 1,
                    subplot_spec=outer[0], wspace=0, hspace=0)

    # --------------------------------------
    #          Look-Locker T1 map
    # --------------------------------------

    ax1 = plt.Subplot(fig, left[0])

    # Layer with image

    bloch_map_m = np.ma.masked_equal(bloch_map, 0)

    im = ax1.imshow(bloch_map_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

    # Add Layer with ROIs
    for i in range(len(rois)):

        # Single color for ROI
        cmap_roi = colors.ListedColormap(COLORS[i])
        roi_tmp = np.ma.masked_equal(rois[i], 0)
        
        # Plot ROI as overlay
        im = ax1.imshow(roi_tmp, origin='lower', cmap=cmap_roi, alpha=0.6)

        # Add arrow pointing to ROI
        ybase = np.max(np.where(1 == roi_tmp)[0])
        xbase = np.max(np.where(1 == roi_tmp)[1])
        ax1.arrow(xbase+20, ybase+20, -12, -12, head_width=5, color=COLORS[i])

    # Recreate Colorbar from image
    im = ax1.imshow(bloch_map_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

    # Ensure same scaling as map with colorbar has
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax)
    cbar.set_label("T$_1$ / s", fontsize=FS)
    cbar.ax.tick_params(labelsize=FS)
    # cax.set_visible(False)

    ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    ax1.xaxis.set_ticks_position('none')
    ax1.yaxis.set_ticks_position('none')
    # ax1.set_axis_off()
    ax1.grid('off')
    ax1.set_xlabel("Bloch Reconstruction", fontsize=FS)

    fig.add_subplot(ax1)

    # --------------------------------------
    #           ROI Analysis
    # --------------------------------------

    bloch_values = []
    bloch_std = []

    for i in rois:

        bval, bstd = perform_roi_analysis(bloch_map, i)
        bloch_values.append(bval)
        bloch_std.append(bstd)

    # --------------------------------------
    #        ROI Analysis Plot
    # --------------------------------------

    right = gridspec.GridSpecFromSubplotSpec(1, 1,
                    subplot_spec=outer[1], wspace=0, hspace=0)
    
    ax4 = plt.Subplot(fig, right[0])
    plt.grid(color='0.15')

    ax4.set_ylim([0, 1.1*max(bloch_values)])

    for i in range(0,len(bloch_values)):
        ax4.errorbar(reft1[i], bloch_values[i], xerr=stdt1[i], yerr=bloch_std[i], fmt='*', color=COLORS[i], label='ROI '+str(i+1))

    ax4.plot([VMIN, VMAX], [VMIN, VMAX], ':', color='gray')

    ulim = np.max([max(reft1), max(bloch_values)])

    ax4.set_ylabel("Bloch T$_1$ / s", fontsize=FS)
    ax4.set_xlabel("GS Reference T$_1$ / s", fontsize=FS)
    
    ax4.set_xlim((VMIN, VMAX))
    ax4.set_ylim((VMIN, VMAX))
    asp = np.diff(ax4.get_xlim())[0] / np.diff(ax4.get_ylim())[0]
    ax4.set_aspect(asp)
    ax4.legend()

    fig.add_subplot(ax4)

    # plt.tight_layout()
    # plt.show(block = False)
    
    fig.savefig(outfile + ".png", bbox_inches='tight', transparent=False)
