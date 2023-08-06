#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 16:13:47 2021

@author: isabel
"""
import numpy as np
#import sys
#import os
#import pickle
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import rc

from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from spectral_image import SpectralImage

#%%

# path_to_results = "C:/Users/abelbrokkelkam/PhD/data/MLdata/results/dE_n10-inse_SI-003/E1_shift09_k10_average/fixed_b/image_KK_4.pkl"
path_to_results = "C:/Users/abelbrokkelkam/PhD/data/MLdata/results/dE_nf-ws2_SI-001/E1_p16_k5_average/fixed_b/image_KK.pkl"
im = SpectralImage.load_spectral_image(path_to_results)

# path_to_image = 'C:/Users/abelbrokkelkam/PhD/data/dmfiles/10n-dop-inse-B1_stem-eels-SI-processed_003.dm4'
# path_to_image = 'C:/Users/abelbrokkelkam/PhD/data/dmfiles/area03-eels-SI-aligned.dm4'
# im = SpectralImage.load_data(path_to_image)

#path_to_models = 'C:/Users/abelbrokkelkam/PhD/data/MLdata/models/dE_nf-ws2_SI-001/E1_p16_k5_average/'
#im.load_zlp_models(path_to_models=path_to_models)
im.pool(5)
im.cluster(5)
im.calc_axes()

#%% Settings for all heatmaps
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'], 'size': 12})
rc('text', usetex=True)

#%%

# InSe general settings
# cmap="coolwarm"
# npix_xtick=24.5
# npix_ytick=12.25
# sig_ticks = 3
# scale_ticks = 1E-3
# tick_int = True
# thicknesslimit = np.nanpercentile(im.t[im.clustered == 0],0)
# mask = im.t[:,:,0] < thicknesslimit
# cb_scale=0.4
# title_specimen = r'$\rm{InSe\;}$'
# save_title_specimen = 'InSe_flake'
# #save_loc = "C:/Users/abelbrokkelkam/PhD/data/MLdata/plots/dE_n10-inse_SI-003/E1_shift09_k10_average/fixed_b/pdfplots/"
# save_loc = "C:/Users/abelbrokkelkam/PhD/data/MLdata/plots/paper/InSe/indirect/"

# im.e0 = 200									# keV
# im.beta = 21.3								# mrad
# im.set_n(3.0)								# refractive index, InSe no background

# WS2 general settings
cmap="coolwarm"
npix_xtick=26.25
npix_ytick=26.25
sig_ticks = 3
scale_ticks = 1E-3
tick_int = True
thicknesslimit = np.nanpercentile(im.t[im.clustered == 2],99)
mask = ((np.isnan([im.t[:,:,0]])[0]) | (im.t[:,:,0] > thicknesslimit))
cb_scale=0.85
title_specimen = r'$\rm{WS_2\;nanoflower\;}$'
save_title_specimen = 'WS2_nanoflower_flake'
# save_loc = "C:/Users/abelbrokkelkam/PhD/data/MLdata/plots/dE_nf-ws2_SI-001//E1_p16_k5_average/fixed_b/pdfplots/"
save_loc = "C:/Users/abelbrokkelkam/PhD/data/MLdata/plots/paper/WS2/"

im.e0       = 200                           # keV
im.beta     = 67.2                          # mrad
im.set_n(4.1462, n_background = 2.1759)     # refractive index, WS2 triangles with SiN substrate as background
im.set_n(4.1462, n_background = 1)          # refractive index, WS2 nanoflower with vacuum as background, note that calculations on SiN may get weird

def round_to_nearest(value, base=5):
    return base * round(float(value) / base)


#%% CLUSTER
im.plot_heatmap(im.clustered, title = title_specimen + r'$\rm{-\;K=10\;clusters\;}$', 
                cbar_kws={'label': r'$\rm{[-]\;}$','shrink':cb_scale}, discrete_colormap = True,
                xlab = r'$\rm{[nm]\;}$', ylab = r'$\rm{[nm]\;}$', cmap = cmap,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Clustered')

#%% THICKNESS
im.plot_heatmap(im.t[:,:,0], title = title_specimen + r"$\rm{-\;Thickness\;}$", 
                cbar_kws={'label': r"$\rm{[nm]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmin=0,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Thickness')

im.plot_heatmap(im.t[:,:,0], title = title_specimen + r"$\rm{-\;Thickness\;}$", 
                cbar_kws={'label': r"$\rm{[nm]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap, 
                mask = mask, vmin = 0, vmax = 60, 
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Thickness_capped')

im.plot_heatmap((im.t[:,:,2]-im.t[:,:,1])/(2*im.t[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Thickness\;}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmin = 0,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Thickness_Error')

im.plot_heatmap((im.t[:,:,2]-im.t[:,:,1])/(2*im.t[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Thickness\;}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmin = 0, vmax = 0.025,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Thickness_Error_capped')

# im.plot_heatmap((im.t[:,:,2]-im.t[:,:,1])/(im.t[:,:,0]), title = title_specimen + " - r"$\rm{-\;Relative\;Broadness\;CI\;Thickness\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmin = 0, vmax = 0.02,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Thickness_CI')
#%% THICKNESS DISCRETIZED

# mask_t = (mask | ((im.t[:,:,2]-im.t[:,:,1])/im.t[:,:,0] >= 1))
# size_t_bins = np.nanpercentile((im.t[:,:,2]-im.t[:,:,1])[~mask_t],100)/0.3
# t_round  = np.round(im.t[:,:,0]/size_t_bins) * size_t_bins
# im.plot_heatmap(t_round, title = title_specimen + r"$\rm{-\;Thickness\;Discretized\;}$",
#                 cbar_kws={'label': r"$\rm{[nm]\;}$",'shrink':0.4}, color_bin_size = size_t_bins, discrete_colormap = True,
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask_t, vmax = 300, vmin = 50,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_thickness_Discretized')

#%% MAX IEELS

im.plot_heatmap(im.max_ieels[:,:,0], title = title_specimen + r"$\rm{-\;Maximum\;IEELS\;}$", 
                cbar_kws={'label': 'Energy loss [eV]','shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Max_IEELS')

im.plot_heatmap((im.max_ieels[:,:,2]-im.max_ieels[:,:,1])/(2*im.max_ieels[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Maximum\;IEELS\;}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmax = 0.001, 
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Max_IEELS_Error')

# im.plot_heatmap((im.max_ieels[:,:,2]-im.max_ieels[:,:,1])/(im.max_ieels[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Maximum\;IEELS\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 0.001,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Max_IEELS_CI')

#%% MAX IEELS DISCRETIZED

mask_max_ieels = (mask | ((im.max_ieels[:,:,2]-im.max_ieels[:,:,1])/im.max_ieels[:,:,0] >= 1))
size_ieels_bins = 1.0 # round_to_nearest(np.nanpercentile((im.max_ieels[:,:,0])[~mask_max_ieels],50)/2,0.5)
ieels_round  = np.round(im.max_ieels[:,:,0]/size_ieels_bins) * size_ieels_bins
im.plot_heatmap(ieels_round, title = title_specimen + r"$\rm{-\;Maximum\;IEELS\;Discretized\;}$", 
                cbar_kws={'label': r"$\rm{Energy\;Loss\;[eV]\;}$", 'shrink':cb_scale}, color_bin_size = size_ieels_bins, discrete_colormap = True,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmin = 21, vmax = 25,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Max_IEELS_Discretized')


#%% THICKNESS CROSSSECTION

fig1, ax1 = plt.subplots(dpi=200)
ax1.set_title(title_specimen + r"$\rm{-\;Thickness\;y\;cross\;section}$")
ax1.set_xlabel(r"$\rm{x-axis\;[nm]\;}$")
ax1.set_ylabel(r"$\rm{Thickness\;[nm]\;}$")
for i in np.arange(5,len(im.y_axis),5):
    row = i
    colors = cm.coolwarm(np.linspace(0,1,len(im.t[0,:,0])))
    ax1.set_prop_cycle(color=colors)
    for j in range(len(im.t[row,:,0]) - 1):
        ax1.plot(im.x_axis[j:j + 2]*scale_ticks, im.t[row,:,0][j:j + 2])
        ax1.fill_between(im.x_axis[j:j + 2]*scale_ticks, im.t[row,:,2][j:j + 2], im.t[row,:,1][j:j + 2], alpha = 0.3)
    
    
#     ax1.plot(im.x_axis, im.t[row,:,0], label = "Row " + str(row))
#     ax1.fill_between(im.x_axis, im.t[row,:,2], im.t[row,:,1], alpha = 0.3)
# ax1.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: int(x*scale_ticks)))
# ax1.legend(loc=2)


fig2, ax2 = plt.subplots(dpi=200)
ax2.set_title(title_specimen + r"$\rm{-\;Thickness\;x\;cross\;section}$")
ax2.set_xlabel(r"$\rm{y-axis\;[nm]\;}$")
ax2.set_ylabel(r"$\rm{Thickness\;[nm]\;}$")
for i in np.arange(5,len(im.x_axis),5):
    column = i
    colors = cm.coolwarm(np.linspace(0,1,len(im.t[0,:,0])))
    ax2.plot(im.y_axis*scale_ticks, im.t[:,column,0], color = colors[i])
    # ax2.plot(im.y_axis, im.t[:,column,0], label = "Column " + str(column), color = colors[i])
    ax2.fill_between(im.y_axis*scale_ticks, im.t[:,column,2], im.t[:,column,1], alpha = 0.3, color = colors[i])
# ax2.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: int(x*scale_ticks)))
# ax2.legend(loc=2)


#%% NUM CROSSINGS

im.n_cross = np.round(im.n_cross)

mask_cross = (mask | (im.n_cross[:,:,0] == 0))

im.plot_heatmap(im.n_cross[:,:,0], title = title_specimen + r"$\rm{-\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Nr.\;Crossings\;}$",'shrink':cb_scale}, discrete_colormap = True,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Crossings')

im.plot_heatmap((im.n_cross[:,:,2]-im.n_cross[:,:,1]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Nr.\;Crossings\;}$",'shrink':cb_scale}, discrete_colormap = True, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Crossings_CI')

# mask_cross = (mask | (im.n_cross[:,:,2] == 0))
# im.plot_heatmap(im.n_cross[:,:,0], title = "Indium Selenide Sample \nCrossings $\u03B5_{1}$ \nAlternative mask", cbar_kws={'label': 'nr. crossings','shrink':0.4}, cmap = cmap, mask = mask_cross, discrete_colormap = True, n_xticks=8, n_yticks=6)
# im.plot_heatmap((im.n_cross[:,:,2]-im.n_cross[:,:,1]), title = "Indium Selenide Sample \nRelative broadness CI Crossings $\u03B5_{1}$ \nAlternative mask", cbar_kws={'label': 'nr. crossings','shrink':0.4}, cmap = cmap, mask = mask_cross, discrete_colormap = True, n_xticks=8, n_yticks=6)


#%% ENERGY AT FIRST CROSSINGS

first_crossings = np.zeros(np.append(im.image_shape, 3))
first_crossings_CI = np.zeros(im.image_shape)
for i in range(im.image_shape[0]):
    for j in range(im.image_shape[1]):
        if type(im.E_cross[i,j]) == np.ndarray:
            if len(im.E_cross[i,j]) > 0:
                first_crossings[i,j,:] = im.E_cross[i,j][0,:]
                first_crossings_CI[i,j] = (im.E_cross[i,j][0,2]-im.E_cross[i,j][0,1])/(2*im.E_cross[i,j][0,0])
        
mask_cross = (mask | (im.n_cross[:,:,0] == 0))        
im.plot_heatmap(first_crossings[:,:,0], title = title_specimen + r"$\rm{-\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross, 
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_Crossings')

im.plot_heatmap(first_crossings_CI, title = title_specimen + r"$\rm{-\;Relative\;Error\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_First_Crossings_Error')

im.plot_heatmap(first_crossings_CI, title = title_specimen + r"$\rm{-\;Relative\;Error\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross, vmax = 0.01,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_First_Crossings_Error_capped')

# im.plot_heatmap(first_crossings_CI, title = title_specimen + r"$\rm{-\;Relative\;Broadness\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask_cross, vmax = 0.01,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Energy_First_Crossings_CI')

# mask_cross = (mask | (im.n_cross[:,:,2] == 0))
# im.plot_heatmap(first_crossings[:,:,0], title = "Indium Selenide Sample \nenergy first crossings $\u03B5_{1}$ \n(for chance at least 1 crossing > 0.1) \nAlternative mask", cbar_kws={'label': 'energy [eV]','shrink':0.4}, cmap = cmap, mask = mask_cross, n_xticks=8, n_yticks=6)
# im.plot_heatmap(first_crossings_CI, title = "Indium Selenide Sample \nrelative broadness CI energy first crossings $\u03B5_{1}$ \n(for chance at least 1 crossing > 0.1) \nAlternative mask", cbar_kws={'label': 'ratio [-]','shrink':0.4}, cmap = cmap, mask = mask_cross, n_xticks=8, n_yticks=6)
# im.plot_heatmap(first_crossings_CI, title = "Indium Selenide Sample \nrelative broadness CI energy first crossings $\u03B5_{1}$ \n(for chance at least 1 crossing > 0.1), capped at 0.005 \nAlternative mask", cbar_kws={'label': 'ratio [-]','shrink':0.4}, vmax = 0.005, cmap = cmap, mask = mask_cross, n_xticks=8, n_yticks=6)

#%% CROSSINGS AT MAX IEELS

mask_max_cross = (mask | (im.n_cross[:,:,0] == 0) | (first_crossings[:,:,0] < 21) | (first_crossings[:,:,0] > 25) )        
im.plot_heatmap(first_crossings[:,:,0], title = title_specimen + r"$\rm{-\;Energy\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_max_cross, vmin = 21, vmax = 25, 
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings')

im.plot_heatmap(first_crossings_CI, title = title_specimen + r"$\rm{-\;Relative\;Error\;Energy\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_max_cross, vmax = 0.01,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings_Error')

# im.plot_heatmap(first_crossings_CI, title = title_specimen + r"$\rm{-\;Relative\;Broadness\;Energy\;Crossings\;}$" + "$\epsilon_{1}$" + r"$\rm{\;IEELS\;Max\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask_cross, vmax = 0.01,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings_CI')

# mask_cross = (mask | (im.n_cross[:,:,2] == 0))
# im.plot_heatmap(first_crossings[:,:,0], title = "Indium Selenide Sample \nenergy first crossings $\u03B5_{1}$ \n(for chance at least 1 crossing > 0.1) \nAlternative mask", cbar_kws={'label': 'energy [eV]','shrink':0.4}, cmap = cmap, mask = mask_cross, n_xticks=8, n_yticks=6)
# im.plot_heatmap(first_crossings_CI, title = "Indium Selenide Sample \nrelative broadness CI energy first crossings $\u03B5_{1}$ \n(for chance at least 1 crossing > 0.1) \nAlternative mask", cbar_kws={'label': 'ratio [-]','shrink':0.4}, cmap = cmap, mask = mask_cross, n_xticks=8, n_yticks=6)
# im.plot_heatmap(first_crossings_CI, title = "Indium Selenide Sample \nrelative broadness CI energy first crossings $\u03B5_{1}$ \n(for chance at least 1 crossing > 0.1), capped at 0.005 \nAlternative mask", cbar_kws={'label': 'ratio [-]','shrink':0.4}, vmax = 0.005, cmap = cmap, mask = mask_cross, n_xticks=8, n_yticks=6)


#%% ENERGY CROSSINGS ??

# first_crossings = np.zeros(np.append(im.image_shape, 3))
# first_crossings_CI = np.zeros(im.image_shape)
# for i in range(im.image_shape[0]):
#     for j in range(im.image_shape[1]):
#         if im.n_cross[i,j,0] > 1:
#             if len(im.n_cross[i,j]) > 0:
#                 first_crossings[i,j,:] = im.n_cross[i,j][0,:]
#                 first_crossings_CI[i,j] = im.n_cross[i,j][0,2]-im.n_cross[i,j][0,1]
#
# im.plot_heatmap(first_crossings[:,:,0], title = "energy first crossing real part dielectric function\n(for chance at least 1 crossing > 0.5)", cbar_kws={'label':  'energy [eV]'}, cmap = cmap)
# im.plot_heatmap(first_crossings_CI, title = "broadness CI energy first crossing real part dielectric function \n(for chance at least 1 crossing > 0.5)", cbar_kws={'label':  'energy [eV]'}, cmap = cmap)


#%% ENERGY CROSSING DISCRETIZED

mask_E_cross = (mask | (im.n_cross[:,:,0] == 0))
size_E_cross_bins = 0.5 #round_to_nearest(np.nanpercentile((first_crossings[:,:,2]-first_crossings[:,:,1])[~mask_E_cross],50)/0.1,1.0)
E_cross_round  = np.round(first_crossings[:,:,0]/size_E_cross_bins) * size_E_cross_bins
im.plot_heatmap(E_cross_round, title = title_specimen + r"$\rm{-\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale}, color_bin_size = size_E_cross_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross, vmin = 21, vmax = 25,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_Crossings_Discretized')

size_E_cross_bins = 0.5 #round_to_nearest(np.nanpercentile((first_crossings[:,:,2]-first_crossings[:,:,1])[~mask_E_cross],50)/0.5,0.5)
E_cross_round  = np.round(first_crossings[:,:,0]/size_E_cross_bins) * size_E_cross_bins
im.plot_heatmap(E_cross_round, title = title_specimen + r"$\rm{-\;Energy\;Max\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale}, color_bin_size = size_E_cross_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_max_cross,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings_Discretized')

size_E_cross_error_bins = 0.001 #round_to_nearest(np.nanpercentile((first_crossings[:,:,2]-first_crossings[:,:,1])[~mask_E_cross],50)/0.1,1.0)
E_cross_error_round  = np.round(first_crossings_CI[:,:]/size_E_cross_error_bins) * size_E_cross_error_bins
im.plot_heatmap(E_cross_error_round, title = title_specimen + r"$\rm{-\;Relative\;Error\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, color_bin_size = size_E_cross_error_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross, vmax = 0.009,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_First_Crossings_Error_discretized')

size_E_cross_error_bins = 0.001 #round_to_nearest(np.nanpercentile((first_crossings[:,:,2]-first_crossings[:,:,1])[~mask_E_cross],50)/0.1,1.0)
E_cross_error_round  = np.round(first_crossings_CI[:,:]/size_E_cross_error_bins) * size_E_cross_error_bins
im.plot_heatmap(E_cross_error_round, title = title_specimen + r"$\rm{-\;Relative\;Error\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, color_bin_size = size_E_cross_error_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_max_cross, vmax = 0.009,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings_Error_discretized')

# mask_E_cross = (mask | (im.n_cross[:,:,2] == 0))
# size_E_cross_bins = np.nanpercentile((first_crossings[:,:,2]-first_crossings[:,:,1])[~mask_cross],50)/0.05
# E_cross_round  = np.round(first_crossings[:,:,0]/size_E_bins) * size_E_bins
# im.plot_heatmap(E_cross_round, title = "Indium Selenide Sample \nenergy first crossing $\u03B5_{1}$ discretized \n(for chance at least 1 crossing > 0.1) \nAlternative mask", cbar_kws={'label': 'energy [eV]','shrink':0.4}, cmap = cmap, mask = mask_E_cross, color_bin_size = size_E_cross_bins, discrete_colormap = True, sig=3, n_xticks=8, n_yticks=6)

#%% DIELECTRIC FUNCTION INDIVIDUAL PIXELS

for i in np.arange(0, 31, 30): # len(im.x_axis)
    for j in np.arange(0, 31, 30): #len(im.y_axis)
        if i != 0 and j != 0:
            pixx=20
            pixy=80
            
            epsilon1 = im.eps[pixy,pixx,0].real
            epsilon2 = im.eps[pixy,pixx,0].imag
            
            fig1, ax1 = plt.subplots(dpi=200)
            ax1.plot(im.deltaE[(len(im.deltaE)-len(epsilon1)):], epsilon1, label = "$\epsilon_{1}$")
            ax1.plot(im.deltaE[(len(im.deltaE)-len(epsilon2)):], epsilon2, label = "$\epsilon_{2}$")
            ax1.axhline(0, color='black')
            ax1.set_title(title_specimen + r"$\rm{-\;Dielectric\;Function\;pixel[%d,%d]}$"%(pixx, pixy))
            ax1.set_xlabel(r"$\rm{Energy\;Loss\;[eV]\;}$")
            ax1.set_ylabel(r"$\rm{Dielectric\;Function\;[F/m]\;}$")
            ax1.set_ylim(-0.2,5)
            ax1.legend()

            plt.savefig(save_loc + save_title_specimen + '_Dielectric_function_pixel[' + str(pixx) + ','+ str(pixy) + '].pdf')
        
#%% BANDGAP

# im.plot_heatmap(im.E_band[:,:,0], title = title_specimen + r"$\rm{-\;Bandgap\;Energy\;}$",
#                 cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_Fixed_b')

# im.plot_heatmap(im.E_band[:,:,0], title = title_specimen + r"$\rm{-\;Bandgap\;Energy\;}$",
#                 cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 1.5,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_Fixed_b_capped')

# im.plot_heatmap((im.E_band[:,:,2]-im.E_band[:,:,1])/(2*im.E_band[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Energy\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_Error_Fixed_b')

# im.plot_heatmap((im.E_band[:,:,2]-im.E_band[:,:,1])/(2*im.E_band[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Energy\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 0.3,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_Error_Fixed_b_capped')


# im.plot_heatmap((im.E_band[:,:,2]-im.E_band[:,:,1])/(im.E_band[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Bandgap\;Energy\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_CI')

# im.plot_heatmap((im.E_band[:,:,2]-im.E_band[:,:,1])/(im.E_band[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Bandgap\;Energy\;}$" + "\n" + r"$\rm{Capped\;at\;0.1\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 0.1,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_CI_capped')

#%% BANDGAP EXPONENT

# im.plot_heatmap(im.b[:,:,0], title = title_specimen + r"$\rm{-\;Bandgap\;Exponent\;}$",
#                 cbar_kws={'label': r"$\rm{[-]\;}$", 'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_exponent')

# im.plot_heatmap(im.b[:,:,0], title = title_specimen + r"$\rm{-\;Bandgap\;Exponent\;}$" + "\n" + r"$\rm{b\;<\;1\;}$",
#                 cbar_kws={'label': r"$\rm{[-]\;}$", 'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmin=0, vmax=1,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_exponent_capped')

# im.plot_heatmap((im.b[:,:,2]-im.b[:,:,1])/(2*im.b[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Exponent\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_exponenent_Error')

# im.plot_heatmap((im.b[:,:,2]-im.b[:,:,1])/(2*im.b[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Exponent\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 1.0,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_exponenent_Error_capped')

# im.plot_heatmap((im.b[:,:,2]-im.b[:,:,1])/(im.b[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Bandgap\;Exponent\;}$",
#                 cbar_kws={'label': 'Ratio [-]','shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_exponenent_CI')

# im.plot_heatmap((im.b[:,:,2]-im.b[:,:,1])/(im.b[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Bandgap\;Exponent\;}$" + "\n" + r"$\rm{Capped\;at\;0.2\;}$",
#                 cbar_kws={'label': 'Ratio [-] ','shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 0.2,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_exponent_CI_capped')

#%% BANDGAP DISCRETIZED

# mask_E_band = (mask | ((im.E_band[:,:,2]-im.E_band[:,:,1])/im.E_band[:,:,0] >= 1))
# size_E_band_bins = 0.1 #round_to_nearest(np.nanpercentile((im.E_band[:,:,2]-im.E_band[:,:,1])[~mask_E_band],50)/8,0.5)
# E_band_round  = np.round(im.E_band[:,:,0]/size_E_band_bins) * size_E_band_bins
# im.plot_heatmap(E_band_round, title = title_specimen + r"$\rm{-\;Bandgap\;Energy\;}$",
#                 cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale}, color_bin_size = size_E_band_bins, discrete_colormap = True, sig_cbar = 2,
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 1.4,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_Discretized_Fixed_b')

# E_band_error = (im.E_band[:,:,2]-im.E_band[:,:,1])/(2*im.E_band[:,:,0])
# size_E_band_error_bins = 0.05 #round_to_nearest(np.nanpercentile((im.E_band[:,:,2]-im.E_band[:,:,1])[~mask_E_band],50)/8,0.5)
# E_band_error_round  = np.round(E_band_error/size_E_band_error_bins) * size_E_band_error_bins
# im.plot_heatmap(E_band_error_round, title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Energy\;}$",
#                 cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, color_bin_size = size_E_band_error_bins, discrete_colormap = True, sig_cbar = 3,
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_Relative_Error_Discretized_Fixed_b')

#%% BANDGAP EXPONENT

# mask_b = (mask | (im.b[:,:,0] == 0))
# size_b_bins = 0.2 #round_to_nearest(np.nanpercentile((im.b[:,:,2]-im.b[:,:,1])[~mask_b],50)/8,0.2)
# b_round  = np.round(im.b[:,:,0]/size_b_bins) * size_b_bins
# im.plot_heatmap(b_round, title = title_specimen + r"$\rm{-\;Bandgap\;Exponent\;}$",
#                 cbar_kws={'label':'[-]','shrink':cb_scale}, color_bin_size = size_b_bins, discrete_colormap = True, sig_cbar = 2,
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 1,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_exponent_Discretized')

# b_error = (im.b[:,:,2]-im.b[:,:,1])/(2*im.b[:,:,0])
# size_b_error_bins = 0.2 #round_to_nearest(np.nanpercentile((im.b[:,:,2]-im.b[:,:,1])[~mask_b],50)/8,0.2)
# b_error_round  = np.round(b_error/size_b_error_bins) * size_b_error_bins
# im.plot_heatmap(b_error_round, title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Exponent\;}$",
#                 cbar_kws={'label':'[-]','shrink':cb_scale}, color_bin_size = size_b_bins, discrete_colormap = True, sig_cbar = 2,
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask, vmax = 1,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_exponent_Discretized')

#%% MSE

# mse_max = np.max(im.mse[:,:,0])
# mse_norm = im.mse[:,:,0] / mse_max
#
#
# im.plot_heatmap(mse_norm, title = title_specimen + r"$\rm{-\;Bandgap\;MSE\;}$",
#                 cbar_kws={'label': r"$\rm{[-]\;}$",'shrink':cb_scale},
#                 xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
#                 mask = mask,
#                 sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
#                 save_as = save_loc + save_title_specimen + '_Bandgap_MSE_Fixed_b')



#%% BANDGAP FIT INDIVIDUAL PIXELS
"""
def bandgap_test(x, amp, BG, b=1.5):
    result = np.zeros(x.shape)
    result[x<BG] = 0
    result[x>=BG] = amp * (x[x>=BG] - BG)**(b)
    return result

for i in np.arange(0, im.image_shape[1], 30):
    for j in np.arange(0, im.image_shape[0], 30):
        if i != 0 and j != 0:
            pixx=i
            pixy=j
            windowlength = 21
            polyorder = 2
            #dE1 = im.dE1[im.clustered]
            
            ieels_p = im.ieels_p[pixy,pixx,0,:]
            ieels_p_smooth = savgol_filter(ieels_p, window_length = windowlength, polyorder = polyorder)
            ieels_p_1d = np.diff(ieels_p_smooth)
            ieels_p_1d_smooth = savgol_filter(ieels_p_1d, window_length = windowlength, polyorder = polyorder)
            
            try:
                range1 = im.deltaE[ieels_p_smooth > 2]
                range1 = range1[range1 > 0][0]
                
                range3 = im.deltaE[np.argwhere(np.diff(np.sign(ieels_p_1d_smooth + 1)))]
                range3 = range3[range3 > range1][0]
                
                range2 = (range3+range1)/2
                #baseline = np.average(IEELSs_fit[(im.deltaE > range1 - 0.1) & (im.deltaE < range1)])
                
                popt, pcov = curve_fit(bandgap_test, im.deltaE[(im.deltaE > range1) & (im.deltaE < range2)], 
                                       ieels_p[(im.deltaE > range1) & (im.deltaE < range2)],
                                       p0 = [300, 1.5], bounds=([0, 0], np.inf))
                
                Amp = popt[0]
                E_bg = popt[1]
                #b = popt[2]
                print("succes! Range1 = " + str(range1) + ", Range2 = " + str(range2))
            except:
                print("frowny face")


            fig2, ax2 = plt.subplots(dpi=200)
            ax2.set_title(title_specimen + r"$\rm{-\;Bandgap\;Fit\;pixel[%d,%d]}$"%(pixx, pixy))
            ax2.set_xlabel(r"$\rm{Energy\;Loss\;[eV]\;}$")
            ax2.set_ylabel(r"$\rm{Intensity\;[a.u.]\;}$")
            ax2.set_ylim(-2,600)
            ax2.set_xlim(1,5)
            
            ax2.fill_between(im.deltaE, im.ieels_p[pixy,pixx,1,:], im.ieels_p[pixy,pixx,2,:], alpha = 0.1, color = 'C0')
            ax2.plot(im.deltaE, ieels_p,label = "Spectrum", alpha = 1.0, color = 'C0')
            ax2.plot(im.deltaE, bandgap_test(im.deltaE, Amp, E_bg), label = r"$\rm{Fit}$", alpha = 1.0, color = 'C1')
            ax2.axhline(0, color = 'black', alpha=0.5)
            ax2.axvspan(xmin=range1, xmax=range2, ymin=-1000, ymax=1000, color = 'C3', alpha=0.1)
            ax2.legend(loc="lower right",frameon=False)

            #plt.savefig(save_loc + save_title_specimen + '_Bandgap_fit_pixel[' + str(pixx) + ','+ str(pixy) + '].pdf')
            
            # Free b
            #print("pixel[" + str(pixx) + ","+ str(pixy) + "] done, dE1 = " + str(round(dE1,4)) + ", BG = " + str(round(popt[1],4)) + ", b = " + str(round(popt[2],4)))
            
            # Fixed b
            print("pixel[" + str(pixx) + ","+ str(pixy) + "] done, BG = " + str(round(popt[1],4)))
            #print("pixel[" + str(pixx) + ","+ str(pixy) + "] done, dE1 = " + str(round(dE1,4)) + ", BG = " + str(round(popt[1],4)))
"""
#%% BANDGAP FIT INDIVIDUAL PIXELS ALL MODELS
"""
def bandgap(x, amp, BG, b = 1.5):
    global baseline
    result = np.zeros(x.shape)
    result[x<BG] = 0
    result[x>=BG] = amp * (x[x>=BG] - BG)**(b)
    return result

#path_to_image = 'C:/Users/abelbrokkelkam/PhD/data/dmfiles/10n-dop-inse-B1_stem-eels-SI-processed_003.dm4'
path_to_image = 'C:/Users/abelbrokkelkam/PhD/data/dmfiles/area03-eels-SI-aligned.dm4'
im = SpectralImage.load_data(path_to_image)

#path_to_models = 'C:/Users/abelbrokkelkam/PhD/data/MLdata/models/dE_n10-inse_SI-003/E1_shift09_k10_average/'
path_to_models = 'C:/Users/abelbrokkelkam/PhD/data/MLdata/models/dE_nf-ws2_SI-001/E1_p16_k5_average/'
im.load_zlp_models(path_to_models=path_to_models)
im.cluster(5)
im.pool(5)
im.calc_axes()

im.e0 = 200									# keV
im.beta = 21.3								# mrad
im.set_n(3.0)								# refractive index, InSe no background
#%%
for i in np.arange(0, 31, 30): # im.image_shape[1]
    for j in np.arange(0, 31, 30): # im.image_shape[0]
        if i != 0 and j != 0:
            pixx=20
            pixy=80
            cluster = im.clustered[pixy,pixx]
            dE1 = im.dE1[1,int(cluster)]
            dE2 = dE1 * 3
            
            #[ts, IEELSs, max_IEELSs], [epss, ts_p, S_ss_p, IEELSs_p, max_IEELSs_p] = im.KK_pixel(pixy, pixx, signal="pooled", iterations=5, select_ZLPs=False)
            
            signal_bg = im.get_pixel_signal(pixy, pixx, signal="pooled")
            ZLPs_match_bg = im.calc_zlps_matched(pixy, pixx, signal="pooled", select_ZLPs=False)
            IEELSs_p_bg = signal_bg - ZLPs_match_bg
            
            hiccup_check = np.max(signal_bg[(im.deltaE > dE1) & (im.deltaE < dE2)])
            hiccup_idx = np.argmax(signal_bg[(im.deltaE > dE1) & (im.deltaE < dE2)])
            idx_hiccup = None
            if hiccup_check > 2000:
                idx_hiccup = np.argmax(signal_bg[(im.deltaE > dE1) & (im.deltaE < dE2)]) + len(signal_bg[im.deltaE <= dE1])
            
            #%%
            n_model         = IEELSs_p_bg.shape[0]
            windowlength    = 21
            polyorder       = 2
            
            IEELSs_p_bg_smooth     = savgol_filter(IEELSs_p_bg, window_length = windowlength, polyorder = polyorder, axis = 1)
            IEELSs_p_bg_1d         = np.diff(IEELSs_p_bg_smooth, axis = 1)
            IEELSs_p_bg_1d_smooth  = savgol_filter(IEELSs_p_bg_1d, window_length = windowlength, polyorder = polyorder, axis = 1)
            #IEELSs_p_2d = np.diff(IEELSs_p_1d_smooth, axis = 1)
            #IEELSs_p_2d_smooth = savgol_filter(IEELSs_p_2d, window_length = windowlength, polyorder = polyorder, axis = 1)
            
            As = []
            E_bands = []
            bs = []
            bandgapfits = []
            
            k_succes = []
            range1list = []
            range2list = []
            
            mselist = []
            for k in range(n_model):
                IEELSs_fit = IEELSs_p_bg[k]
                IEELSs_fit_smooth = IEELSs_p_bg_smooth[k]
                
                try:
                    range1 = dE1 * 0.85
                    #range1 = 0.7*dE1
                    
                    #range1 = im.deltaE[IEELSs_fit_smooth > 15]
                    #range1 = range1[range1 > 0][0]
                    
                    #range3 = im.deltaE[np.argwhere(np.diff(np.sign(IEELSs_p_1d_smooth[k] + 1)))]
                    #range3 = range3[range3 > range1]
                    #range3 = range3[range3 > dE1][0]
                    
                    #range2 = (range3+range1)/2
                    
                    range2 = range1 + 1.0
                    
                    deltaE_filter = (im.deltaE > range1) & (im.deltaE < range2)
                    
                    if idx_hiccup is not None:
                        hiccup_filter = (im.deltaE > im.deltaE[idx_hiccup - 5]) & (im.deltaE < im.deltaE[idx_hiccup + 5])
                        
                        for i in range(len(deltaE_filter)):
                            if deltaE_filter[i] == True and hiccup_filter[i] == True:
                                deltaE_filter[i] = False
                    
                    fit_domain_x = im.deltaE[deltaE_filter]
                    fit_domain_y = IEELSs_fit[deltaE_filter]
                    #baseline = np.average(IEELSs_fit[(im.deltaE > range1 - 0.1) & (im.deltaE < range1)])
                    baseline = np.average(IEELSs_fit[(im.deltaE < range1)])
                    
                    popt, pcov = curve_fit(bandgap, fit_domain_x, fit_domain_y, 
                                           p0 = [IEELSs_fit[im.deltaE >= range2][0], range1], 
                                           bounds=([0, 0], np.inf))
                    
                    As.append(popt[0])
                    E_bands.append(popt[1])
                    #bs.append(popt[2])
                    
                    bandgapfits.append(bandgap(im.deltaE, popt[0], popt[1]))
                    #bandgapfits.append(bandgap_test(im.deltaE, popt[0], popt[1], popt[2]))
                    
                    k_succes.append(k)
                    range1list.append(range1)
                    range2list.append(range2)
                    
                    mse_value = np.mean(np.square(bandgap(fit_domain_x, *popt) - fit_domain_y))
                    mselist.append(mse_value)
                    print("succes!")
                except:
                    #n_fails += 1
                    #print("fail nr.: ", n_fails, "failed curve-fit, row: ", row, ", pixel: ", j, ", model: ", i)
                    print("frowny face")
            
            As = np.array(As)
            E_bands = np.array(E_bands)
            bs = np.array(bs)
            bandgapfits = np.array(bandgapfits)
            range1list = np.array(range1list)
            range2list = np.array(range2list)
            k_succes = np.array(k_succes)
            mselist = np.array(mselist)
            #%%
            #title_specimen = r'$\rm{InSe\;}$'
            #save_title_specimen = 'InSe'
            #save_loc = "C:/Users/abelbrokkelkam/PhD/data/MLdata/plots/paper/InSe/"
            
            title_specimen = r'$\rm{WS_2\;nanoflower\;}$'
            save_title_specimen = 'WS2_nanoflower_flake'
            save_loc = "C:/Users/abelbrokkelkam/PhD/data/MLdata/plots/paper/WS2/"
            import random
            
            
            fig2, ax2 = plt.subplots(dpi=200)
            ax2.set_title(title_specimen + r"$\rm{-\;Bandgap\;Fit\;pixel[%d,%d]}$"%(pixx, pixy))
            ax2.set_xlabel(r"$\rm{Energy\;Loss\;[eV]\;}$")
            ax2.set_ylabel(r"$\rm{Intensity\;[a.u.]\;}$")
            ax2.set_ylim(-2,500)
            ax2.set_xlim(1,5)
            
            ax2.fill_between(im.deltaE, np.nanpercentile(IEELSs_p_bg_smooth, 16, axis = 0), np.nanpercentile(IEELSs_p_bg_smooth, 84, axis = 0), alpha = 0.1, color = 'C0')
            #ax2.fill_between(im.deltaE[1:], np.nanpercentile(IEELSs_p_1d_smooth, 16, axis = 0), np.nanpercentile(IEELSs_p_1d_smooth, 84, axis = 0), alpha = 0.1, color = 'C1')
            #ax2.fill_between(im.deltaE[1:-1], np.nanpercentile(IEELSs_p_2d_smooth, 16, axis = 0), np.nanpercentile(IEELSs_p_2d_smooth, 84, axis = 0), alpha = 0.1, color = 'C2')
            #ax2.plot(im.deltaE, np.nanpercentile(IEELSs_p_bg, 50, axis = 0),label=r"$\rm{Median\;all\;model}$", alpha = 0.1, color = 'C0')
            ax2.plot(im.deltaE, np.nanpercentile(IEELSs_p_bg_smooth, 50, axis = 0),label=r"$\rm{Median\;substracted\;spectra}$", alpha = 0.5, color = 'C0')
            #ax2.plot(im.deltaE[1:], np.nanpercentile(IEELSs_p_1d_smooth, 50, axis = 0), alpha = 0.5, color = 'C1')
            #ax2.plot(im.deltaE[1:-1], np.nanpercentile(IEELSs_p_2d_smooth, 50, axis = 0), alpha = 0.5, color = 'C2')
            
            
            # Plot individual models
            
            for k in range(1):
                r = random.random()
                g = random.random()
                b = random.random()
                color = 'C1'#(r ,g ,b)
                bg_idx = np.random.randint(0, len(k_succes))
                ax2.plot(im.deltaE, bandgapfits[bg_idx], color=color,label=r"$\rm{Fit\;single\;model}$")
                ax2.plot(im.deltaE, IEELSs_p_bg[k_succes[bg_idx]], color=color, alpha=0.1)
                ax2.plot(im.deltaE, IEELSs_p_bg_smooth[k_succes[bg_idx]], color=color, alpha=0.5)
                ax2.axvspan(xmin=range1list[bg_idx], xmax=range2list[bg_idx], ymin=-1000, ymax=1000, color = color, alpha=0.1)
                #ax2.text(x=0.1,y=350,s=r"$\rm{Amp\;=\;%.2f\;}$"%(As[bg_idx]))
                #ax2.text(x=0.1,y=320,s=r"$\rm{Ebg\;=\;%.2f\;eV}$"%(E_bands[bg_idx]))
                #ax2.text(x=0.1,y=290,s=r"$\rm{b\;=\;%.2f}$"%(bs[bg_idx]))
                #ax2.text(x=0.1,y=290,s=r"$\rm{MSE\;=\;%.2f}$"%(mselist[bg_idx]))
                print(bg_idx)
                print(range1, range2)
            
            ax2.fill_between(im.deltaE, np.nanpercentile(bandgapfits, 16, axis = 0), np.nanpercentile(bandgapfits, 84, axis = 0), alpha = 0.1, color = 'C2')
            # ax2.fill_between(im.deltaE,
            #                 bandgap_test(im.deltaE, np.nanpercentile(As, 16, axis = 0),np.nanpercentile(E_bands, 16, axis = 0),np.nanpercentile(bs, 16, axis = 0)),
            #                 bandgap_test(im.deltaE, np.nanpercentile(As, 84, axis = 0),np.nanpercentile(E_bands, 84, axis = 0),np.nanpercentile(bs, 84, axis = 0)),
            #                 alpha = 0.2, color = 'C5')
            # ax2.plot(im.deltaE, np.nanpercentile(bandgapfits, 50, axis = 0),label = "median bandgapfits", alpha = 1.0, color = 'C4')
            # ax2.plot(im.deltaE, bandgap_test(im.deltaE, np.nanpercentile(As, 50, axis = 0),np.nanpercentile(E_bands, 50, axis = 0),np.nanpercentile(bs, 50, axis = 0)),label = r"$\rm{median\;parameters}$", alpha = 1.0, color = 'C4')
            ax2.plot(im.deltaE, bandgap(im.deltaE, np.nanpercentile(As, 50, axis = 0),np.nanpercentile(E_bands, 50, axis = 0)),label = r"$\rm{Fit\;median\;parameters}$", alpha = 1.0, color = 'C2', linestyle='--')
            #ax2.text(x=0.1,y=250,s=r"$\rm{MSE\;Median\;=\;%.2f}$"%(np.nanpercentile(mselist, 50, axis = 0)))
            ax2.axhline(0,color = 'black', alpha=0.5)
            #ax2.axvspan(xmin=np.nanpercentile(range1, 50, axis = 0), xmax=np.nanpercentile(range2, 50, axis = 0), ymin=-1000, ymax=1000, color = 'C3', alpha=0.1)
            ax2.legend(loc=4,frameon=False)

            fig2.savefig(save_loc + save_title_specimen + '_Bandgap_fit_pixel[' + str(pixx) + ','+ str(pixy) + '].pdf')
            
            #print("pixel[" + str(pixx) + ","+ str(pixy) + "] done, dE1 = " + str(round(dE1,4)) + ", BG = " + str(round(popt[1],4)))
            #print("pixel[" + str(pixx) + ","+ str(pixy) + "] done, dE1 = " + str(round(dE1,4)) + ", BG = " + str(round(popt[1],4)) + ", b = " + str(round(popt[2],4)))
            #print("pixel[" + str(pixx) + ","+ str(pixy) + "] done, dE1 = " + str(round(dE1,4)) + ", BG = " + str(round(popt2[1],4)) + ", b = " + str(round(popt2[2],4)) + " (smooth)")
            
            # Fixed b
            #print("pixel[" + str(pixx) + ","+ str(pixy) + "] done, dE1 = " + str(round(dE1,4)) + ", BG = " + str(round(popt[1],4)))
            #print("pixel[" + str(pixx) + ","+ str(pixy) + "] done, dE1 = " + str(round(dE1,4)) + ", BG = " + str(round(popt2[1],4)) + " (smooth)")
"""
#%% EPSILON

"""
eps = im.eps[30,30,0,:]
eps_1 = eps.real
eps_2 = eps.imag
deltaE_eps = np.arange(0,len(eps)*15, 15)/1000

#eps_1_DM = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Epsilon_1_pixel_30_30_m3d038_to_26d422.txt')
#eps_2_DM = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Epsilon_2_pixel_30_30_m3d038_to_26d422.txt')
eps_1_DM = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Epsilon_1_pixel_30_30_m3d038_to_26d422_single_iter_reftail.txt')
eps_2_DM = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Epsilon_2_pixel_30_30_m3d038_to_26d422_single_iter_reftail.txt')

eps_1_DM_n20 = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Epsilon_1_pixel_30_30_m3d038_to_26d422_20_iter_reftail.txt')
eps_2_DM_n20 = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Epsilon_2_pixel_30_30_m3d038_to_26d422_20_iter_reftail.txt')


#eps_1_DM_n1 = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Epsilon_1_pixel_30_30_m3d038_to_26d422_single_iter.txt')
#eps_2_DM_n1 = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Epsilon_1_pixel_30_30_m3d038_to_26d422_single_iter.txt')

fig3, ax3 = plt.subplots(dpi=200)
fig4, ax4 = plt.subplots(dpi=200)
ax3.set_title("epsilon 1 pixel[30,30]")
ax3.set_xlabel("energy loss [eV]")
#ax3.set_ylabel("Crossings")
ax4.set_title("epsilon 2 pixel[30,30]")
ax4.set_xlabel("energy loss [eV]")
#ax4.set_ylabel("Crossings")
ax3.set_ylim(-1,7)
ax4.set_ylim(0,6)
#ax3.set_xlim(-3,5)
#ax3.fill_between(im.deltaE, p_low, p_high, alpha = 0.2)
ax3.plot(deltaE_eps, eps_1, label = "EELSfitter")
ax3.plot(im.deltaE, eps_1_DM, label = "DM, n=1")
ax3.plot(im.deltaE, eps_1_DM_n20, label = "DM, n=20")
ax3.axhline(y=0, color='black', linestyle='-')
ax4.plot(deltaE_eps, eps_2, label = "EELSfitter")
ax4.plot(im.deltaE, eps_2_DM, label = "DM, n=1")
ax4.plot(im.deltaE, eps_2_DM_n20, label = "DM, n=20")
ax4.axhline(y=0, color='black', linestyle='-')

ax3.legend()
ax4.legend()
"""
#%% Surface loss function and intensity
"""
Surloss_func_n1 = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Surface-loss-function_pixel_30_30_m3d038_to_26d422_single_iter_reftail.txt')
Surloss_func_n20 = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Surface-loss-function_pixel_30_30_m3d038_to_26d422_20_iter_reftail.txt')

Surloss_int_n1 = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Surface-loss-intensity_pixel_30_30_m3d038_to_26d422_single_iter_reftail.txt')
Surloss_int_n20 = np.loadtxt('C:/Users/abelbrokkelkam/PhD/data/m20210331/eels/eels-SI/10n_dop_inse-B1_stem-eels-SI-processed_003_Surface-loss-intensity_pixel_30_30_m3d038_to_26d422_20_iter_reftail.txt')


fig5, ax5 = plt.subplots(dpi=200)
fig6, ax6 = plt.subplots(dpi=200)
ax5.set_title("Surface-Loss function pixel[30,30]")
ax5.set_xlabel("energy loss [eV]")
#ax5.set_ylabel("Crossings")
ax6.set_title("Surface-Loss intensity pixel[30,30]")
ax6.set_xlabel("energy loss [eV]")
#ax6.set_ylabel("Crossings")
#ax5.set_ylim(-1,7)
#ax6.set_ylim(0,6)
#ax5.set_xlim(-3,5)
#ax5.fill_between(im.deltaE, p_low, p_high, alpha = 0.2)
#ax5.plot(deltaE_eps, eps_1, label = "EELSfitter")
ax5.plot(im.deltaE, Surloss_func_n1, label = "n=1")
ax5.plot(im.deltaE, Surloss_func_n20, label = "n=20")
ax5.axhline(y=0, color='black', linestyle='-')
#ax6.plot(deltaE_eps, eps_2, label = "EELSfitter")
ax6.plot(im.deltaE, Surloss_int_n1, label = "n=1")
ax6.plot(im.deltaE, Surloss_int_n20, label = "n=20")
ax6.axhline(y=0, color='black', linestyle='-')

ax5.legend()
ax6.legend()
"""
#%%

