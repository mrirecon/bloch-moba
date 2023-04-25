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
VMAXT2 = 0.75

VMIN = 0


BCOLOR='white'  # Background color
TCOLOR='black'  # Text color

def perform_roi_analysis(paramap, roi):

    segment = paramap * roi

    # Set zeros to be invalid for mean calculation
    segment_m = np.ma.masked_equal(segment, 0)

    return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

        #Error if wrong number of parameters
        if (len(sys.argv) == 5):
                print( "Plotting" )
                print( "#-----------------------------------------------" )
                print( "Usage: create_figure.py <ref NIST> <T1 reco> <T2 reco> <ROIS> <outfile>" )
                exit()

        sysargs = sys.argv

        # Load reference data
        reft1, reft2 = np.loadtxt(sysargs[1], unpack=True)
        
        # Load Bloch T1 reco
        bloch_t1 = np.abs(cfl.readcfl(sysargs[2]).squeeze())
        bloch_t1[bloch_t1 == np.inf] = 0

        # Load Bloch T2 reco
        bloch_t2 = np.abs(cfl.readcfl(sysargs[3]).squeeze())
        bloch_t2[bloch_t2 == np.inf] = 0

        rois = np.abs(cfl.readcfl(sysargs[4]).squeeze())
        rois[rois == np.inf] = 0

        # Define output filename
        outfile = sysargs[5]


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
                for i in range(0, np.shape(rois)[2]):

                        tmp_roi = rois[:,:,i]

                        bval, bstd = perform_roi_analysis(t1_data, tmp_roi)
                        bloch_values_t1.append(bval)
                        bloch_std_t1.append(bstd)

                        bval, bstd = perform_roi_analysis(t2_data, tmp_roi)
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

        fig = plt.figure(num = 1, figsize=(30, 10), dpi=120)

        outer = gridspec.GridSpec(1, 2, wspace=-0.3, hspace=0)

        left = gridspec.GridSpecFromSubplotSpec(2, 1,
                        subplot_spec=outer[0], wspace=0, hspace=0.3)

        # --------------------------------------
        #          Bloch T1 map
        # --------------------------------------

        ax1 = plt.Subplot(fig, left[0])

        # Layer with image

        bloch_t1_m = np.ma.masked_equal(bloch_t1[:,:,2], 0)     # Take HypSec with SP reco

        im = ax1.imshow(bloch_t1_m, cmap=my_cmap, vmax=VMAXT1, vmin=VMIN)

        # Add Layer with ROIs
        for i in range(1, np.shape(rois)[2]):

                # Single color for ROI
                cmap_roi = colors.ListedColormap(WBC)
                roi_tmp = np.ma.masked_equal(rois[:,:,i], 0)
                
                # Plot ROI as overlay
                im = ax1.imshow(roi_tmp, cmap=cmap_roi, alpha=0.6)

                # Add arrow pointing to ROI
                ybase = np.max(np.where(1 == roi_tmp)[0])
                xbase = np.max(np.where(1 == roi_tmp)[1])
                ax1.text(xbase, ybase+1, str(i), fontsize=FS, fontweight='bold', color='black')

        # Recreate Colorbar from image
        im = ax1.imshow(bloch_t1_m, visible=False, cmap=my_cmap, vmax=VMAXT1, vmin=VMIN)

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
        ax1.text(-0.3*np.shape(bloch_t1_m)[0], -0.1*np.shape(bloch_t1_m)[0], 'A', fontsize=FS+14, fontweight='bold', color=TCOLOR)
        ax1.text(-0.15*np.shape(bloch_t1_m)[0], -0.1*np.shape(bloch_t1_m)[0], "$\\bf{Simulated~Data}$", fontsize=FS+2, fontweight='bold', color=TCOLOR)


        fig.add_subplot(ax1)

        # --------------------------------------
        #          Bloch T2 map
        # --------------------------------------

        ax2 = plt.Subplot(fig, left[1])

        my_cmap2 = copy.copy(cm.get_cmap('turbo'))
        my_cmap2.set_bad(BCOLOR)

        bloch_t2_m = np.ma.masked_equal(bloch_t2[:,:,2], 0)     # Take HypSec with SP reco

        im = ax2.imshow(np.flip(bloch_t2_m, axis=0), origin='lower', cmap=my_cmap2, vmax=VMAXT2, vmin=VMIN)

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





        # --------------------------------------
        #        ROI Analysis Plot T1 
        #               - Perfect Inv., No SP
        # --------------------------------------

        ind = 0 # Perfect Inv., No SP

        right = gridspec.GridSpecFromSubplotSpec(2, 3,
                        subplot_spec=outer[1], wspace=-0.2, hspace=0.3)

        ax3 = plt.Subplot(fig, right[0])

        for i in range(1,len(t1[ind])):
                ax3.errorbar(reft1[i], t1[ind][i], yerr=t1_std[ind][i], fmt='*', markersize= MS, color=COLORS[i-1], label='ROI: '+str(i))

        ax3.plot([VMIN, VMAXT1], [VMIN, VMAXT1], ':', color='gray')

        ulim = np.max([max(reft1), max(t1[ind])])

        # ax3.set_ylabel("$\\bf{Bloch}$ $\\bf{T}$$_1$ / s", fontsize=FS+5)
        # ax3.set_xlabel("$\\bf{Reference}$ T$_1$ / s", fontsize=FS+3)

        ax3.set_title("$\\bf{Perfect~Inversion}$", fontsize=FS+2, pad=10)

        ax3.tick_params(labelsize=FS+3)
        ax3.set_xlim((VMIN, VMAXT1))
        ax3.set_ylim((VMIN, VMAXT1))
        asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0] * 0.9 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
        ax3.set_aspect(asp)
        ax3.locator_params(axis='x', nbins=4)
        ax3.legend()
        ax3.grid(alpha=0.2)

        for axis in ['top','bottom','left','right']:
                ax3.spines[axis].set_linewidth(2)
        ax3.tick_params(width=2)

        fig.add_subplot(ax3)

        # --------------------------------------
        #        ROI Analysis Plot T2
        #               - Perfect Inv., No SP
        # --------------------------------------
        
        ax4 = plt.Subplot(fig, right[3])

        for i in range(1,len(t1[ind])):
                ax4.errorbar(reft2[i], t2[ind][i], yerr=t2_std[ind][i], fmt='*', markersize= MS, color=COLORS[i-1], label='ROI: '+str(i))

        ax4.plot([VMIN, VMAXT2], [VMIN, VMAXT2], ':', color='gray')

        ulim = np.max([max(reft2), max(t2[ind])])

        # ax4.set_ylabel("$\\bf{Bloch}$ $\\bf{T}$$_2$ / s", fontsize=FS+5)
        # ax4.set_xlabel("$\\bf{Reference}$ T$_2$ / s", fontsize=FS+3)
        ax4.tick_params(labelsize=FS+3)
        ax4.set_xlim((VMIN, VMAXT2))
        ax4.set_ylim((VMIN, VMAXT2))
        asp = np.diff(ax4.get_xlim())[0] / np.diff(ax4.get_ylim())[0] * 0.9 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
        ax4.set_aspect(asp)
        ax4.locator_params(axis='x', nbins=4)
        # ax4.legend()
        ax4.grid(alpha=0.2)

        for axis in ['top','bottom','left','right']:
                ax4.spines[axis].set_linewidth(2)
        ax4.tick_params(width=2)

        fig.add_subplot(ax4)

        # --------------------------------------
        #        ROI Analysis Plot T1 
        #               - Perfect Inv., SP
        # --------------------------------------

        ind = 1 # Perfect Inv., SP

        ax6 = plt.Subplot(fig, right[1])

        for i in range(1,len(t1[ind])):
                ax6.errorbar(reft1[i], t1[ind][i], yerr=t1_std[ind][i], fmt='*', markersize= MS, color=COLORS[i-1], label='ROI: '+str(i))

        ax6.plot([VMIN, VMAXT1], [VMIN, VMAXT1], ':', color='gray')

        ulim = np.max([max(reft1), max(t1[ind])])

        # ax6.set_ylabel("$\\bf{Bloch}$ T$_1$ / s", fontsize=FS)
        ax6.set_xlabel("$\\bf{Reference}$ T$_1$ / s", fontsize=FS+3)

        ax6.set_title("$\\bf{Slice}$", fontsize=FS+2, pad=10)

        ax6.tick_params(labelsize=FS+3)
        ax6.set_xlim((VMIN, VMAXT1))
        ax6.set_ylim((VMIN, VMAXT1))
        asp = np.diff(ax6.get_xlim())[0] / np.diff(ax6.get_ylim())[0] * 0.9 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
        ax6.set_aspect(asp)
        ax6.locator_params(axis='x', nbins=4)
        # ax6.legend()
        ax6.grid(alpha=0.2)

        ax6.set_yticklabels([])

        for axis in ['top','bottom','left','right']:
                ax6.spines[axis].set_linewidth(2)
        ax6.tick_params(width=2)

        fig.add_subplot(ax6)

        # --------------------------------------
        #        ROI Analysis Plot T2
        #               - Perfect Inv., SP
        # --------------------------------------
        
        ax7 = plt.Subplot(fig, right[4])

        for i in range(1,len(t1[ind])):
                ax7.errorbar(reft2[i], t2[ind][i], yerr=t2_std[ind][i], fmt='*', markersize= MS, color=COLORS[i-1], label='ROI: '+str(i))

        ax7.plot([VMIN, VMAXT2], [VMIN, VMAXT2], ':', color='gray')

        ulim = np.max([max(reft2), max(t2[ind])])

        # ax7.set_ylabel("$\\bf{Bloch}$ T$_2$ / s", fontsize=FS)
        ax7.set_xlabel("$\\bf{Reference}$ T$_2$ / s", fontsize=FS+3)
        ax7.tick_params(labelsize=FS+3)
        ax7.set_xlim((VMIN, VMAXT2))
        ax7.set_ylim((VMIN, VMAXT2))
        asp = np.diff(ax7.get_xlim())[0] / np.diff(ax7.get_ylim())[0] * 0.9 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
        ax7.set_aspect(asp)
        ax7.locator_params(axis='x', nbins=4)
        # ax7.legend()
        ax7.grid(alpha=0.2)

        ax7.set_yticklabels([])

        for axis in ['top','bottom','left','right']:
                ax7.spines[axis].set_linewidth(2)
        ax7.tick_params(width=2)

        fig.add_subplot(ax7)

        # --------------------------------------
        #        T2 Inset Plot
        # --------------------------------------

        # Create a set of inset Axes: these should fill the bounding box allocated to them.
        ax8 = plt.axes([0,0,0.99,0.99])

        # Manually set the position and relative size of the inset axes within ax1
        ip2 = InsetPosition(ax7, [0.55,0.2,0.4,0.3]) # xmin, xmax, ymin, ymax
        ax8.set_axes_locator(ip2)
        
        for i in range(1,len(t1[ind])):
                ax8.errorbar(reft2[i], t2[ind][i], yerr=t2_std[ind][i], fmt='*', markersize= MS, color=COLORS[i-1], label='ROI: '+str(i))

        ax8.plot([VMIN, VMAXT2], [VMIN, VMAXT2], ':', color='gray')
        
        # Automatic estimation of inset location
        max_val = 0.11 #1.1*np.max(reft2[1:-2])

        ax8.axis([0, max_val, 0, max_val])
        # ax8.locator_params(axis='both', nbins=2)
        ax8.tick_params(labelsize=FS-3)



        # --------------------------------------
        #        ROI Analysis Plot T1 
        #               - HypSec Inv., SP
        # --------------------------------------

        ind = 2 # HyperSec, SP

        ax9 = plt.Subplot(fig, right[2])

        for i in range(1,len(t1[ind])):
                ax9.errorbar(reft1[i], t1[ind][i], yerr=t1_std[ind][i], fmt='*', markersize= MS, color=COLORS[i-1], label='ROI: '+str(i))

        ax9.plot([VMIN, VMAXT1], [VMIN, VMAXT1], ':', color='gray')

        ulim = np.max([max(reft1), max(t1[ind])])

        # ax9.set_ylabel("$\\bf{Bloch}$ T$_1$ / s", fontsize=FS)
        # ax9.set_xlabel("$\\bf{Reference}$ T$_1$ / s", fontsize=FS+3)

        ax9.set_title("$\\bf{Pulse~+~Slice}$", fontsize=FS+2, pad=10)

        ax9.tick_params(labelsize=FS+3)
        ax9.set_xlim((VMIN, VMAXT1))
        ax9.set_ylim((VMIN, VMAXT1))
        asp = np.diff(ax9.get_xlim())[0] / np.diff(ax9.get_ylim())[0] * 0.9 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
        ax9.set_aspect(asp)
        ax9.locator_params(axis='x', nbins=4)
        # ax9.legend()
        ax9.grid(alpha=0.2)

        ax9.set_yticklabels([])

        for axis in ['top','bottom','left','right']:
                ax9.spines[axis].set_linewidth(2)
        ax9.tick_params(width=2)

        fig.add_subplot(ax9)

        # --------------------------------------
        #        ROI Analysis Plot T2
        #               - HypSec Inv., SP
        # --------------------------------------
        
        ax10 = plt.Subplot(fig, right[5])

        for i in range(1,len(t1[ind])):
                ax10.errorbar(reft2[i], t2[ind][i], yerr=t2_std[ind][i], fmt='*', markersize= MS, color=COLORS[i-1], label='ROI '+str(i))

        ax10.plot([VMIN, VMAXT2], [VMIN, VMAXT2], ':', color='gray')

        ulim = np.max([max(reft2), max(t2[ind])])

        # ax10.set_ylabel("$\\bf{Bloch}$ T$_2$ / s", fontsize=FS)
        # ax10.set_xlabel("$\\bf{Reference}$ T$_2$ / s", fontsize=FS+3)
        ax10.tick_params(labelsize=FS+3)
        ax10.set_xlim((VMIN, VMAXT2))
        ax10.set_ylim((VMIN, VMAXT2))
        asp = np.diff(ax10.get_xlim())[0] / np.diff(ax10.get_ylim())[0] * 0.9 # Colorbar reduces aspect ratio of imshow plot. 0.93 compensates for difference
        ax10.set_aspect(asp)
        ax10.locator_params(axis='x', nbins=4)
        # ax10.legend()
        ax10.grid(alpha=0.2)

        ax10.set_yticklabels([])

        for axis in ['top','bottom','left','right']:
                ax10.spines[axis].set_linewidth(2)
        ax10.tick_params(width=2)

        fig.add_subplot(ax10)

        # --------------------------------------
        #        T2 Inset Plot
        # --------------------------------------

        # Create a set of inset Axes: these should fill the bounding box allocated to them.
        ax11 = plt.axes([0,0,0.999,0.999])

        # Manually set the position and relative size of the inset axes within ax1
        ip3 = InsetPosition(ax10, [0.55,0.2,0.4,0.3]) # xmin, xmax, ymin, ymax
        ax11.set_axes_locator(ip3)

        for i in range(1,len(t1[ind])):
                ax11.errorbar(reft2[i], t2[ind][i], yerr=t2_std[ind][i], fmt='*', markersize= MS, color=COLORS[i-1], label='ROI '+str(i))

        ax11.plot([VMIN, VMAXT2], [VMIN, VMAXT2], ':', color='gray')
        
        # Automatic estimation of inset location
        max_val = 0.11 # 1.1*np.max(reft2[1:-5])

        ax11.axis([0, max_val, 0, max_val])
        ax11.tick_params(labelsize=FS-3)

        # plt.tight_layout()
        
        fig.savefig(outfile + ".png", bbox_inches='tight', transparent=False)
