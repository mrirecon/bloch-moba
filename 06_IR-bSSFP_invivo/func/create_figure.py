#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

FS=28

COLORS = ['darkorange', 'r', 'g', 'b', 'm', 'y', 'c', 'k', 'w']

DARK = 0 #dark layout?

VMAX = 2.9
VMAX2 = 0.08
VMIN = 0

DIFF_SCALING = 1


BCOLOR='white'  # Background color
TCOLOR='black'  # Text color



def perform_roi_analysis(paramap, roi):

        segment = paramap * roi

        # Set zeros to be invalid for mean calculation
        segment_m = np.ma.masked_equal(segment, 0)

        return segment_m.mean(), segment_m.std()



if __name__ == "__main__":

        #Error if wrong number of parameters
        if( len(sys.argv) < 7):
                print( "Plotting" )
                print( "#-----------------------------------------------" )
                print( "Usage: create_figure.py <LL T1 map> <Bloch T1 map> <outfile> <ROI 1> ... <ROI N>" )
                exit()

        sysargs = sys.argv

        # Load maps
        ll_map = np.abs(cfl.readcfl(sysargs[1]).squeeze())
        ll_map[ll_map == np.inf] = 0
        
        bloch_short_t1 = np.abs(cfl.readcfl(sysargs[2]).squeeze())
        bloch_short_t1[bloch_short_t1 == np.inf] = 0

        bloch_short_t2 = np.abs(cfl.readcfl(sysargs[3]).squeeze())
        bloch_short_t2[bloch_short_t2 == np.inf] = 0

        bloch_long_t1 = np.abs(cfl.readcfl(sysargs[4]).squeeze())
        bloch_long_t1[bloch_long_t1 == np.inf] = 0

        bloch_long_t2 = np.abs(cfl.readcfl(sysargs[5]).squeeze())
        bloch_long_t2[bloch_long_t2 == np.inf] = 0


        # Define output filename
        outfile = sysargs[6]

        # Load and stack all passed ROIs
        print("Passed ROIs are:")

        rois = []

        for i in sysargs[7:]:
        
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
                BCOLOR='black'
                TCOLOR='white'
        else:
                plt.style.use(['default'])

        my_cmap = copy.copy(cm.get_cmap('viridis'))
        my_cmap.set_bad(BCOLOR)

        my_cmap2 = copy.copy(cm.get_cmap('turbo'))
        my_cmap2.set_bad(BCOLOR)
        


        fig = plt.figure(num = 1, figsize=(22, 22), dpi=120, edgecolor='w')

        left = gridspec.GridSpec(3, 3, wspace=0, hspace=0.05, figure=fig)

        # --------------------------------------
        #          Look-Locker T1 map
        # --------------------------------------

        # ax1 = plt.Subplot(fig, left[0])

        ax1 = fig.add_subplot(left[0])

        # Layer with image

        ll_map_m = np.ma.masked_equal(ll_map, 0)

        im = ax1.imshow(ll_map_m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

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
                # ax1.arrow(xbase+20, ybase+20, -12, -12, head_width=5, color=COLORS[i])
                ax1.text(xbase+10, ybase, 'ROI '+str(i+1), fontsize=FS+5, fontweight='bold', color=COLORS[i])

        # Recreate Colorbar from image
        im = ax1.imshow(ll_map_m, origin='lower', visible=False, cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cax.set_visible(False)

        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.xaxis.set_ticks_position('none')
        ax1.yaxis.set_ticks_position('none')
        # ax1.set_axis_off()

        ax1.set_title("IR FLASH\n$\\bf{Bloch}$ $\\bf{Model}$", fontsize=FS+5)

        ax1.text(0.03*np.shape(ll_map_m)[0], 0.03*np.shape(ll_map_m)[0], '$\\bf{T}_{1,F}$', fontsize=FS+5, color=TCOLOR)

        fig.add_subplot(ax1)

        # --------------------------------------
        #           Bloch T1 map short
        # --------------------------------------

        ax2 = fig.add_subplot(left[1])

        bloch_short_t1m = np.ma.masked_equal(bloch_short_t1, 0)

        im2 = ax2.imshow(bloch_short_t1m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cax.set_visible(False)

        ax2.set_yticklabels([])
        ax2.set_xticklabels([])
        ax2.xaxis.set_ticks_position('none')
        ax2.yaxis.set_ticks_position('none')
        # ax2.set_axis_off()

        ax2.set_title("IR bSSFP\n$\\bf{Short}$ $\\bf{RF}$", fontsize=FS+5)
        # ax2.set_ylabel("short RF", fontsize=FS)

        ax2.text(0.03*np.shape(bloch_short_t1m)[0], 0.03*np.shape(bloch_short_t1m)[0], '$\\bf{T}_{1,B}$', fontsize=FS+5, color=TCOLOR)

        fig.add_subplot(ax2)

        # --------------------------------------
        #           Bloch T1 map long
        # --------------------------------------

        ax2 = fig.add_subplot(left[2])

        bloch_long_t1m = np.ma.masked_equal(bloch_long_t1, 0)

        im2 = ax2.imshow(bloch_long_t1m, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cax.set_visible(False)

        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im2, cax=cax)
        cbar.set_label("T$_1$ / s", fontsize=FS)
        cbar.ax.tick_params(labelsize=FS)

        ax2.set_yticklabels([])
        ax2.set_xticklabels([])
        ax2.xaxis.set_ticks_position('none')
        ax2.yaxis.set_ticks_position('none')
        # ax2.set_axis_off()

        ax2.set_title("IR bSSFP\n$\\bf{Long}$ $\\bf{RF}$", fontsize=FS+5)

        ax2.text(0.03*np.shape(bloch_long_t1m)[0], 0.03*np.shape(bloch_long_t1m)[0], '$\\bf{T}_{1,B}$', fontsize=FS+5, color=TCOLOR)

        fig.add_subplot(ax2)

        # --------------------------------------
        # Difference between Look-Locker and Bloch T1 map
        # --------------------------------------

        ax3 = fig.add_subplot(left[4])

        diff_map = np.abs(ll_map - bloch_short_t1)

        diff_map_m = np.ma.masked_equal(diff_map, 0)

        im3 = ax3.imshow(diff_map_m*DIFF_SCALING, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Create colorbar and remove it to keep same scaling as other figures
        divider = make_axes_locatable(ax3)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im2, cax=cax)
        cbar.set_label("Diff(T$_1$) / s", fontsize=FS)
        cbar.ax.tick_params(labelsize=FS)
        cbar.remove() 

        # Add scaling as text to Diff image
        # ax3.text(0.85*np.shape(diff_map)[0], 0.01*np.shape(diff_map)[0], 'x'+str(DIFF_SCALING), fontsize=FS+5, color=TCOLOR)

        ax3.set_yticklabels([])
        ax3.set_xticklabels([])
        ax3.xaxis.set_ticks_position('none')
        ax3.yaxis.set_ticks_position('none')
        # ax3.set_axis_off()

        ax3.text(0.03*np.shape(diff_map_m)[0], 0.03*np.shape(diff_map_m)[0], '$|\\bf{T}_{1,F}-\\bf{T}_{1,B}|$', fontsize=FS, color=TCOLOR)

        fig.add_subplot(ax3)

        
        # --------------------------------------
        # Difference between Look-Locker and Bloch T1 map
        # --------------------------------------

        ax3 = fig.add_subplot(left[5])

        diff_map = np.abs(ll_map - bloch_long_t1)

        diff_map_m = np.ma.masked_equal(diff_map, 0)

        im3 = ax3.imshow(diff_map_m*DIFF_SCALING, origin='lower', cmap=my_cmap, vmax=VMAX, vmin=VMIN)

        # Create colorbar and remove it to keep same scaling as other figures
        divider = make_axes_locatable(ax3)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im2, cax=cax)
        cbar.set_label("Diff(T$_1$) / s", fontsize=FS)
        cbar.ax.tick_params(labelsize=FS)
        cbar.remove() 

        # Add scaling as text to Diff image
        # ax3.text(0.85*np.shape(diff_map)[0], 0.01*np.shape(diff_map)[0], 'x'+str(DIFF_SCALING), fontsize=FS+5, color=TCOLOR)

        ax3.set_yticklabels([])
        ax3.set_xticklabels([])
        ax3.xaxis.set_ticks_position('none')
        ax3.yaxis.set_ticks_position('none')
        # ax3.set_axis_off()

        fig.add_subplot(ax3)

        # Add Difference label
        ax3.text(0.03*np.shape(diff_map_m)[0], 0.03*np.shape(diff_map_m)[0], '$|\\bf{T}_{1,F}-\\bf{T}_{1,B}|$', fontsize=FS, color=TCOLOR)


        # --------------------------------------
        #           Bloch T2 map short
        # --------------------------------------

        ax2 = fig.add_subplot(left[7])

        bloch_short_t2m = np.ma.masked_equal(bloch_short_t2, 0)

        im2 = ax2.imshow(bloch_short_t2m, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cax.set_visible(False)

        ax2.set_yticklabels([])
        ax2.set_xticklabels([])
        ax2.xaxis.set_ticks_position('none')
        ax2.yaxis.set_ticks_position('none')
        # ax2.set_axis_off()

        ax2.text(0.03*np.shape(bloch_short_t2m)[0], 0.03*np.shape(bloch_short_t2m)[0], '$\\bf{T}_2$', fontsize=FS+5, color=TCOLOR)

        # ax2.set_ylabel("short RF", fontsize=FS)

        fig.add_subplot(ax2)

        # --------------------------------------
        #           Bloch T2 map long
        # --------------------------------------

        ax2 = fig.add_subplot(left[8])

        bloch_long_t2m = np.ma.masked_equal(bloch_long_t2, 0)

        im2 = ax2.imshow(bloch_long_t2m, origin='lower', cmap=my_cmap2, vmax=VMAX2, vmin=VMIN)

        # Ensure same scaling as map with colorbar has
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cax.set_visible(False)

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

        ax2.text(0.03*np.shape(bloch_long_t2m)[0], 0.03*np.shape(bloch_long_t2m)[0], '$\\bf{T}_2$', fontsize=FS+5, color=TCOLOR)

        fig.add_subplot(ax2)

        # --------------------------------------
        #           ROI Analysis
        # --------------------------------------

        ll_values = []
        ll_std = []
        bloch_s_values_t1 = []
        bloch_s_std_t1 = []
        bloch_s_values_t2 = []
        bloch_s_std_t2 = []
        bloch_l_values_t1 = []
        bloch_l_std_t1 = []
        bloch_l_values_t2 = []
        bloch_l_std_t2 = []

        for i in rois:

                lval, lstd = perform_roi_analysis(ll_map, i)
                ll_values.append(lval)
                ll_std.append(lstd)

                bval, bstd = perform_roi_analysis(bloch_short_t1, i)
                bloch_s_values_t1.append(bval)
                bloch_s_std_t1.append(bstd)

                bval2, bstd2 = perform_roi_analysis(bloch_long_t1, i)
                bloch_l_values_t1.append(bval2)
                bloch_l_std_t1.append(bstd2)

                bval, bstd = perform_roi_analysis(bloch_short_t2, i)
                bloch_s_values_t2.append(bval)
                bloch_s_std_t2.append(bstd)

                bval2, bstd2 = perform_roi_analysis(bloch_long_t2, i)
                bloch_l_values_t2.append(bval2)
                bloch_l_std_t2.append(bstd2)

        # --------------------------------------
        #        Table with ROI Analysis for T1
        # --------------------------------------
        # from matplotlib import rc
        ax1 = fig.add_subplot(left[3])

        plt.rc('text', usetex=True)
        plt.rcParams['font.size'] = '26'

        text=r'''{\renewcommand{\arraystretch}{1.2}\begin{tabular}{c|c|c} $T_1$ [s] & \textbf{ROI 1} & \textbf{ROI 2} \\\hline''' \
                + ''' IR FLASH & ''' \
                + str(np.round(ll_values[0],3)) +'$\pm$'+str(ceil(ll_std[0]*1000)/1000 ) \
                + '''&''' \
                + str(np.round(ll_values[1],3)) +'$\pm$'+str(ceil(ll_std[1]*1000)/1000 ) \
                + r'''\\''' \
                + ''' Short RF & ''' \
                + str(np.round(bloch_s_values_t1[0],3)) +'$\pm$'+str(ceil(bloch_s_std_t1[0]*1000)/1000 ) \
                + '''&''' \
                + str(np.round(bloch_s_values_t1[1],3)) +'$\pm$'+str(ceil(bloch_s_std_t1[1]*1000)/1000 ) \
                + r'''\\''' \
                + ''' Long RF & ''' \
                + str(np.round(bloch_l_values_t1[0],3)) +'$\pm$'+str(ceil(bloch_l_std_t1[0]*1000)/1000 ) \
                + '''&''' \
                + str(np.round(bloch_l_values_t1[1],3)) +'$\pm$'+str(ceil(bloch_l_std_t1[1]*1000)/1000 ) \
                + '''\end{tabular}}'''

        ax1.text(0.48,0.5, text, ha="center", va="center", transform=ax1.transAxes)

        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.xaxis.set_ticks_position('none')
        ax1.yaxis.set_ticks_position('none')
        ax1.set_axis_off()


        # --------------------------------------
        #        Table with ROI Analysis for T2
        # --------------------------------------
        # from matplotlib import rc
        ax1 = fig.add_subplot(left[6])

        plt.rc('text', usetex=True)
        plt.rcParams['font.size'] = '28'

        text=r'''{\renewcommand{\arraystretch}{1.2}\begin{tabular}{c|c|c} $T_2$ [s] & \textbf{ROI 1} & \textbf{ROI 2} \\\hline''' \
                + ''' Short RF & ''' \
                + str(np.round(bloch_s_values_t2[0],3)) +'$\pm$'+str(ceil(bloch_s_std_t2[0]*1000)/1000 ) \
                + '''&''' \
                + str(np.round(bloch_s_values_t2[1],3)) +'$\pm$'+str(ceil(bloch_s_std_t2[1]*1000)/1000 ) \
                + r'''\\''' \
                + ''' Long RF & ''' \
                + str(np.round(bloch_l_values_t2[0],3)) +'$\pm$'+str(ceil(bloch_l_std_t2[0]*1000)/1000 ) \
                + '''&''' \
                + str(np.round(bloch_l_values_t2[1],3)) +'$\pm$'+str(ceil(bloch_l_std_t2[1]*1000)/1000 ) \
                + '''\end{tabular}}'''

        ax1.text(0.48,0.5, text, ha="center", va="center", transform=ax1.transAxes)

        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.xaxis.set_ticks_position('none')
        ax1.yaxis.set_ticks_position('none')
        ax1.set_axis_off()

        fig.savefig(outfile + '.png', bbox_inches='tight', transparent=False)
