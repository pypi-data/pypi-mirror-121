#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import rc
# import seaborn as sns
import numpy as np
from spectral_image import SpectralImage
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
import torch

import sys
import os

rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'], 'size': 10})
rc('text', usetex=True)

# plt.rcParams.update({'font.size': 10})

#path_to_image = '/Users/jaco/Documents/CBL-ML/EELS_KK/dmfiles/10n-dop-inse-B1_stem-eels-SI-processed_003.dm4'
path_to_image = '/Users/jaco/Documents/CBL-ML/EELS_KK/dmfiles/area03-eels-SI-aligned.dm4'
im = SpectralImage.load_data(path_to_image)
#im.output_path = '/Users/jaco/Documents/CBL-ML/EELS_KK/output/InSe_de1_09_300K_run_2'
im.output_path = '/Users/jaco/Documents/CBL-ML/EELS_KK/output/WS2/free_b/'
#im.output_path = '/data/theorie/jthoeve/EELSfitter/output/InSe_p5_10_clusters/'
if not os.path.exists(im.output_path):
    os.makedirs(im.output_path)

path_to_models = '/Users/jaco/Documents/CBL-ML/EELS_KK/models/WS2_p16_5_clusters'
#path_to_models = '/Users/jaco/Documents/CBL-ML/EELS_KK/models/InSe_de1_09_300K_run_2'
#path_to_models = '/data/theorie/jthoeve/EELSfitter/output/models/InSe_p5_10_clusters'
#path_to_results = "/Users/jaco/Documents/CBL-ML/EELS_KK/output/InSe_de1_09_300K_run_2/image_KK_full.pkl"
#path_to_results = "/Users/jaco/Documents/CBL-ML/EELS_KK/output/WS2/image_KK.pkl"
#im = SpectralImage.load_spectral_image(path_to_results)
im.load_zlp_models(path_to_models=path_to_models, plot_chi2=False)

im.pool(5)
im.cluster(5)
sig = "pooled"

# %% General settings

#InSe
# title_specimen = r'$\rm{InSe\;}$'
# save_title_specimen = "InSe"
# save_loc = "/Users/jaco/Documents/CBL-ML/EELS_KK/output/plots_InSe/"
# cmap = "coolwarm"
# npix_xtick = 24.5
# npix_ytick = 12.25
# sig_ticks = 3
# scale_ticks = 1E-3
# tick_int = True
# #thicknesslimit = np.nanpercentile(im.t[im.clustered == 0], 0)
# #mask = im.t[:, :, 0] < thicknesslimit
# cb_scale = 0.4
#
# im.e0 = 200  # keV
# im.beta = 21.3  # mrad
# im.set_n(3.0)  # refractive index, InSe no background

# WS2
title_specimen = r'$\rm{WS_2\;nanoflower\;}$'
save_title_specimen = 'WS2_nanoflower_flake'
save_loc = "/Users/jaco/Documents/CBL-ML/EELS_KK/output/WS2/free_b/"

cmap="coolwarm"
npix_xtick=26.25
npix_ytick=26.25
sig_ticks = 3
scale_ticks = 1E-3
tick_int = True
#thicknesslimit = np.nanpercentile(im.t[im.clustered == 2],99)
#mask = ((np.isnan([im.t[:,:,0]])[0]) | (im.t[:,:,0] > thicknesslimit))
cb_scale=0.85

im.e0       = 200                           # keV
im.beta     = 67.2                          # mrad
#im.set_n(4.1462, n_background = 2.1759)     # refractive index, WS2 triangles with SiN substrate as background
im.set_n(4.1462, n_background = 1)          # refractive index, WS2 nanoflower with vacuum as background, note that calculations on SiN may get weird

# %%
# plot zlp prediction
#print(im.image_shape)
im.plot_inel_pred(pixx=125, pixy=39, title_specimen=r"$\rm{InSe}$")

# %%
# plot array of subplots zlp + signal
im.plot_zlp_signal()

# %%
# plot zlp for cluster means
im.output_path = '/Users/jaco/Documents/CBL-ML/EELS_KK/output/WS2'
im.plot_zlp_ntot()



#%% CLUSTER
im.plot_heatmap(im.clustered, title = title_specimen + r'$\rm{-\;K=10\;clusters\;}$',
                cbar_kws={'label': r'$\rm{[cluster\;ID]\;}$','shrink':cb_scale}, discrete_colormap = True,
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
                mask = mask, vmin = 0, vmax = 0.03,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Thickness_Error_capped')
"""
im.plot_heatmap((im.t[:,:,2]-im.t[:,:,1])/(im.t[:,:,0]), title = title_specimen + " - r"$\rm{-\;Relative\;Broadness\;CI\;Thickness\;}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmin = 0, vmax = 0.02,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Thickness_CI')
"""

#%%
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
"""
im.plot_heatmap((im.max_ieels[:,:,2]-im.max_ieels[:,:,1])/(im.max_ieels[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Maximum\;IEELS\;}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmax = 0.001, 
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Max_IEELS_CI')
"""

#%% MAX IEELS DISCRETIZED

mask_max_ieels = (mask | ((im.max_ieels[:,:,2]-im.max_ieels[:,:,1])/im.max_ieels[:,:,0] >= 1))
size_ieels_bins = 1.0 # round_to_nearest(np.nanpercentile((im.max_ieels[:,:,0])[~mask_max_ieels],50)/2,0.5)
ieels_round  = np.round(im.max_ieels[:,:,0]/size_ieels_bins) * size_ieels_bins
im.plot_heatmap(ieels_round, title = title_specimen + r"$\rm{-\;Maximum\;IEELS\;Discretized\;}$",
                cbar_kws={'label': r"$\rm{Energy\;Loss\;[eV]\;}$", 'shrink':cb_scale}, color_bin_size = size_ieels_bins, discrete_colormap = True,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmin = 21, vmax = 26,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Max_IEELS_Discretized')

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
first_crossings = np.zeros(np.append(im.image_shape, 3))
first_crossings_CI = np.zeros(im.image_shape)
for i in range(im.image_shape[0]):
    for j in range(im.image_shape[1]):
        if type(im.E_cross[i, j]) == np.ndarray:
            if len(im.E_cross[i, j]) > 0:
                first_crossings[i, j, :] = im.E_cross[i, j][0, :]
                first_crossings_CI[i, j] = (im.E_cross[i, j][0, 2] - im.E_cross[i, j][0, 1]) / (
                            2 * im.E_cross[i, j][0, 0])

mask_cross = (mask | (im.n_cross[:, :, 0] == 0))
im.plot_heatmap(first_crossings[:, :, 0],
                title=title_specimen + r"$\rm{-\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$",
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$", 'shrink': cb_scale},
                xlab=r"$\rm{[nm]\;}$", ylab=r"$\rm{[nm]\;}$", cmap=cmap,
                mask=mask_cross,
                sig_ticks=sig_ticks, scale_ticks=scale_ticks, npix_xtick=npix_xtick, npix_ytick=npix_ytick,
                tick_int=tick_int,
                save_as=save_loc + save_title_specimen + '_Energy_Crossings')

im.plot_heatmap(first_crossings_CI,
                title=title_specimen + r"$\rm{-\;Relative\;Error\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$",
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$", 'shrink': cb_scale},
                xlab=r"$\rm{[nm]\;}$", ylab=r"$\rm{[nm]\;}$", cmap=cmap,
                mask=mask_cross, vmax=0.2,
                sig_ticks=sig_ticks, scale_ticks=scale_ticks, npix_xtick=npix_xtick, npix_ytick=npix_ytick,
                tick_int=tick_int,
                save_as=save_loc + save_title_specimen + '_Energy_First_Crossings_CI')
"""
im.plot_heatmap(first_crossings_CI, title = title_specimen + r"$\rm{-\;Relative\;Broadness\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross, vmax = 0.01,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_First_Crossings_CI')
"""

mask_max_cross = (mask | (im.n_cross[:,:,0] == 0) | (first_crossings[:,:,0] < 20) | (first_crossings[:,:,0] > 25) )
im.plot_heatmap(first_crossings[:,:,0], title = title_specimen + r"$\rm{-\;Energy\;Crossings\;}$" + "$\epsilon_{1}$" + r"$\rm{\;IEELS\;Max\;}$",
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_max_cross, vmin = 21, vmax = 25,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings')

im.plot_heatmap(first_crossings_CI, title = title_specimen + r"$\rm{-\;Relative\;Error\;Energy\;Crossings\;}$" + "$\epsilon_{1}$" + r"$\rm{\;IEELS\;Max\;}$",
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_max_cross, vmax = 0.2,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings_CI')

"""
im.plot_heatmap(first_crossings_CI, title = title_specimen + r"$\rm{-\;Relative\;Broadness\;Energy\;Crossings\;}$" + "$\epsilon_{1}$" + r"$\rm{\;IEELS\;Max\;}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross, vmax = 0.01,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings_CI')
"""

#%% ENERGY CROSSING DISCRETIZED

mask_E_cross = (mask | (im.n_cross[:,:,0] == 0))
size_E_cross_bins = 4.0 #round_to_nearest(np.nanpercentile((first_crossings[:,:,2]-first_crossings[:,:,1])[~mask_E_cross],50)/0.1,1.0)
E_cross_round  = np.round(first_crossings[:,:,0]/size_E_cross_bins) * size_E_cross_bins
im.plot_heatmap(E_cross_round, title = title_specimen + r"$\rm{-\;Energy\;First\;Crossings\;}$" + "$\epsilon_{1}$",
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale}, color_bin_size = size_E_cross_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_cross,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Energy_Crossings_Discretized')

mask_E_cross = (mask | (im.n_cross[:,:,0] == 0))
size_E_cross_bins = 1.0 #round_to_nearest(np.nanpercentile((first_crossings[:,:,2]-first_crossings[:,:,1])[~mask_E_cross],50)/0.5,0.5)
E_cross_round  = np.round(first_crossings[:,:,0]/size_E_cross_bins) * size_E_cross_bins
im.plot_heatmap(E_cross_round, title = title_specimen + r"$\rm{-\;Energy\;Max\;Crossings\;}$" + "$\epsilon_{1}$",
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale}, color_bin_size = size_E_cross_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask_max_cross,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Energy_Max_Crossings_Discretized')

for i in np.arange(0, len(im.x_axis), 30):
    for j in np.arange(0, len(im.y_axis), 30):
        if i != 0 and j != 0:
            pixx = i
            pixy = j

            epsilon1 = im.eps[pixy, pixx, 0].real
            epsilon2 = im.eps[pixy, pixx, 0].imag

            fig1, ax1 = plt.subplots(dpi=200)
            ax1.plot(im.deltaE[(len(im.deltaE) - len(epsilon1)):], epsilon1, label="$\epsilon_{1}$")
            ax1.plot(im.deltaE[(len(im.deltaE) - len(epsilon2)):], epsilon2, label="$\epsilon_{2}$")
            ax1.axhline(0, color='black')
            ax1.set_title(title_specimen + r"$\rm{-\;Dielectric\;Function\;pixel[%d,%d]}$" % (pixx, pixy))
            ax1.set_xlabel(r"$\rm{Energy\;Loss\;[eV]\;}$")
            ax1.set_ylabel(r"$\rm{Dielectric\;Function\;[F/m]\;}$")
            ax1.set_ylim(-0.2, 5)
            ax1.legend()

            plt.savefig(
                save_loc + save_title_specimen + '_Dielectric_function_pixel[' + str(pixx) + ',' + str(pixy) + '].pdf')
#%% BANDGAP
im.plot_heatmap(im.E_band[:,:,0], title = title_specimen + r"$\rm{-\;Bandgap\;Energy\;}$",
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_Free_b')

im.plot_heatmap((im.E_band[:,:,2]-im.E_band[:,:,1])/(2*im.E_band[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Energy\;}$",
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_Error_Free_b')

im.plot_heatmap((im.E_band[:,:,2]-im.E_band[:,:,1])/(2*im.E_band[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Energy\;}$",
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmax=0.2,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_Error_Free_b_capped')
"""
im.plot_heatmap((im.E_band[:,:,2]-im.E_band[:,:,1])/(im.E_band[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Bandgap\;Energy\;}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap, 
                mask = mask,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Bandgap_CI')

im.plot_heatmap((im.E_band[:,:,2]-im.E_band[:,:,1])/(im.E_band[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Bandgap\;Energy\;}$" + "\n" + r"$\rm{Capped\;at\;0.1\;}$", 
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmax = 0.1, 
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Bandgap_CI_capped')
"""
#%% BANDGAP EXPONENT

im.plot_heatmap(im.b[:,:,0], title = title_specimen + r"$\rm{-\;Bandgap\;Exponent\;}$",
                cbar_kws={'label': r"$\rm{[-]\;}$", 'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_exponent')

im.plot_heatmap(im.b[:,:,0], title = title_specimen + r"$\rm{-\;Bandgap\;Exponent\;}$" + "\n" + r"$\rm{b\;[1,2]\;}$",
                cbar_kws={'label': r"$\rm{[-]\;}$", 'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmin=1, vmax=2,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_exponent_capped')

im.plot_heatmap((im.b[:,:,2]-im.b[:,:,1])/(2*im.b[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Exponent\;}$",
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_exponenent_Error')

im.plot_heatmap((im.b[:,:,2]-im.b[:,:,1])/(2*im.b[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Exponent\;}$",
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale},
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmax = 1.0,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_exponenent_Error_capped')

"""
im.plot_heatmap((im.b[:,:,2]-im.b[:,:,1])/(im.b[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Bandgap\;Exponent\;}$", 
                cbar_kws={'label': 'Ratio [-]','shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, 
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Bandgap_exponenent_CI')

im.plot_heatmap((im.b[:,:,2]-im.b[:,:,1])/(im.b[:,:,0]), title = title_specimen + r"$\rm{-\;Relative\;Broadness\;CI\;Bandgap\;Exponent\;}$" + "\n" + r"$\rm{Capped\;at\;0.2\;}$", 
                cbar_kws={'label': 'Ratio [-] ','shrink':cb_scale}, 
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmax = 0.2,  
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int, 
                save_as = save_loc + save_title_specimen + '_Bandgap_exponent_CI_capped')
"""
#%% BANDGAP DISCRETIZED


mask_E_band = (mask | ((im.E_band[:,:,2]-im.E_band[:,:,1])/im.E_band[:,:,0] >= 1))
size_E_band_bins = 0.2 #round_to_nearest(np.nanpercentile((im.E_band[:,:,2]-im.E_band[:,:,1])[~mask_E_band],50)/8,0.5)
E_band_round  = np.round(im.E_band[:,:,0]/size_E_band_bins) * size_E_band_bins
im.plot_heatmap(E_band_round, title = title_specimen + r"$\rm{-\;Bandgap\;Energy\;}$",
                cbar_kws={'label': r"$\rm{Energy\;[eV]\;}$",'shrink':cb_scale}, color_bin_size = size_E_band_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_Discretized_Free_b')

E_band_error = (im.E_band[:,:,2]-im.E_band[:,:,1])/(2*im.E_band[:,:,0])
size_E_band_error_bins = 0.04 #round_to_nearest(np.nanpercentile((im.E_band[:,:,2]-im.E_band[:,:,1])[~mask_E_band],50)/8,0.5)
E_band_error_round  = np.round(E_band_error/size_E_band_error_bins) * size_E_band_error_bins
im.plot_heatmap(E_band_error_round, title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Energy\;}$",
                cbar_kws={'label': r"$\rm{Ratio\;[-]\;}$",'shrink':cb_scale}, color_bin_size = size_E_band_error_bins, discrete_colormap = True, sig_cbar = 3,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmax= 0.3,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_Relative_Error_Discretized_Free_b')

#%% BANDGAP EXPONENT

mask_b = (mask | (im.b[:,:,0] == 0))
size_b_bins = 0.2 #round_to_nearest(np.nanpercentile((im.b[:,:,2]-im.b[:,:,1])[~mask_b],50)/8,0.2)
b_round  = np.round(im.b[:,:,0]/size_b_bins) * size_b_bins
im.plot_heatmap(b_round, title = title_specimen + r"$\rm{-\;Bandgap\;Exponent\;}$",
                cbar_kws={'label':'[-]','shrink':cb_scale}, color_bin_size = size_b_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmax = 2,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_exponent_Discretized')

b_error = (im.b[:,:,2]-im.b[:,:,1])/(2*im.b[:,:,0])
size_b_error_bins = 0.02 #round_to_nearest(np.nanpercentile((im.b[:,:,2]-im.b[:,:,1])[~mask_b],50)/8,0.2)
b_error_round  = np.round(b_error/size_b_error_bins) * size_b_error_bins
im.plot_heatmap(b_error_round, title = title_specimen + r"$\rm{-\;Relative\;Error\;Bandgap\;Exponent\;}$",
                cbar_kws={'label':'[-]','shrink':cb_scale}, color_bin_size = size_b_bins, discrete_colormap = True, sig_cbar = 2,
                xlab = r"$\rm{[nm]\;}$", ylab = r"$\rm{[nm]\;}$", cmap = cmap,
                mask = mask, vmin = 0,
                sig_ticks = sig_ticks, scale_ticks = scale_ticks, npix_xtick = npix_xtick, npix_ytick = npix_ytick, tick_int = tick_int,
                save_as = save_loc + save_title_specimen + '_Bandgap_exponent_Discretized')

# %% BANDGAP FIT INDIVIDUAL PIXELS

def bandgap_test(x, amp, BG, b):
    global baseline
    result = np.zeros(x.shape)
    result[x < BG] = baseline
    result[x >= BG] = baseline + amp * (x[x >= BG] - BG) ** (b)
    return result


for i in np.arange(0, 61, 60):
    for j in np.arange(0, 31, 30):
        if i != 0 and j != 0:
            pixx = 30
            pixy = 30
            # [ts, IEELSs, max_IEELSs], [epss, ts_p, S_ss_p, IEELSs_p, max_IEELSs_p] = im.KK_pixel(pixy, pixx,
            #                                                                                      signal="pooled",
            #                                                                                      iterations=5,
            #                                                                                      select_ZLPs=False)
            signal = im.get_pixel_signal(pixy, pixx, signal="pooled")
            ZLPs_match = im.calc_zlps_matched(pixy, pixx, signal="pooled", select_ZLPs=False)
            IEELSs_p = signal - ZLPs_match





            n_model = IEELSs_p.shape[0]

# %%
            windowlength = 21
            polyorder = 2

            IEELSs_p_smooth = savgol_filter(IEELSs_p, window_length=windowlength, polyorder=polyorder, axis=1)
            IEELSs_p_1d = np.diff(IEELSs_p_smooth, axis=1)
            IEELSs_p_1d_smooth = savgol_filter(IEELSs_p_1d, window_length=windowlength, polyorder=polyorder, axis=1)
            IEELS_1d_CL_high = np.percentile(IEELSs_p_1d_smooth, 16, axis=0)
            IEELS_1d_CL_high_idx = np.argwhere(np.diff(np.sign(IEELS_1d_CL_high - 0.1)))

            IEELSs_p_2d = np.diff(IEELSs_p_1d_smooth, axis = 1)
            IEELSs_p_2d_smooth = savgol_filter(IEELSs_p_2d, window_length = windowlength, polyorder = polyorder, axis = 1)
            # IEELS_2d_CL_high = np.percentile(IEELSs_p_2d_smooth, 16, axis = 0)
            # IEELS_2d_CL_high_idx = np.argwhere(np.diff(np.sign(IEELS_2d_CL_high)))
            # IEELS_2d_CL_high_idx = IEELS_2d_CL_high_idx[IEELS_2d_CL_high_idx > IEELS_1d_CL_high_idx[0][0]]


            # %%
            # range1 = 0 #im.deltaE[IEELS_1d_CL_high_idx[0][0]]

            As = []
            E_bands = []
            bs = []
            bandgapfits = []

            As_bs_pcov = []
            As_E_bands_pcov = []

            # As_smooth = []
            # E_bands_smooth = []
            # bs_smooth = []
            # bandgapfits_smooth = []

            i_succes = []
            range1list = []
            range2list = []
            for i in range(n_model):

                IEELSs_fit = IEELSs_p[i]
                IEELSs_fit_smooth = IEELSs_p_smooth[i]
                dE1 = im.dE1[1,im.clustered[pixy, pixx]]
                dE2 = 3*dE1

                range1 = 0.85*dE1
                #range1 = im.deltaE[IEELSs_fit_smooth > 200]
                #range1 = range1[range1 > 0][0]

                range3 = im.deltaE[np.argwhere(np.diff(np.sign(IEELSs_p_1d_smooth[i] + 1)))]
                range3 = range3[range3 > range1]
                range3 = range3[range3 > dE1][0]
                range2 = range1 + 0.7 #(range3 + range1) / 2

                # range3 = im.deltaE[np.argwhere(np.diff(np.sign(IEELSs_p_1d_smooth[i] + 1)))]
                # range3 = range3[range3 > range1][0]

                #range2 = range3#(range3 + range1) / 2
                #range2 = range1 + 1 #(range3 + range1) / 2
                # print(range1,range2)

                try:
                    #baseline = np.average(IEELSs_fit[(im.deltaE < range1)])
                    baseline = np.average(IEELSs_p[:, im.deltaE < range1])
                    #baseline_idx = np.argwhere(im.deltaE > range1)[0]
                    #baseline = IEELSs_fit_smooth[baseline_idx][0]
                    c_idx = np.argwhere(im.deltaE > range2)[0]
                    c_init = IEELSs_fit[c_idx][0]

                    popt, pcov = curve_fit(bandgap_test, im.deltaE[(im.deltaE > range1) & (im.deltaE < range2)],
                                           IEELSs_fit_smooth[(im.deltaE > range1) & (im.deltaE < range2)],
                                           p0 = [c_init, range1, 0.5], bounds = ([0, 0, 0], np.inf))

                    # popt2, pcov2 = curve_fit(bandgap_test, im.deltaE[(im.deltaE > range1) & (im.deltaE < range2)],
                    #                       IEELSs_fit_smooth[(im.deltaE > range1) & (im.deltaE < range2)])
                    # p0 = [400, 1.5, 1.5], bounds=([0, 0, 0], np.inf)
                    # if popt[1] >= (range2+range1)/2:
                    #    print("long face")
                    #    continue

                    As.append(popt[0])
                    E_bands.append(popt[1])
                    bs.append(popt[2])

                    # As_E_bands_pcov.append(pcov[0][1])
                    # As_bs_pcov.append(pcov[0][2])

                    # As_smooth.append(popt2[0])
                    # E_bands_smooth.append(popt2[1])
                    # bs_smooth.append(popt2[2])

                    #bandgapfits.append(bandgap_test(im.deltaE, popt[0], popt[1]))
                    bandgapfits.append(bandgap_test(im.deltaE, popt[0], popt[1], popt[2]))
                    # bandgapfits_smooth.append(bandgap_test(im.deltaE, popt2[0], popt2[1], popt2[2]))
                    i_succes.append(i)
                    range1list.append(range1)
                    range2list.append(range2)
                    print("succes!")
                except:

                    print("frowny face")


            As = np.array(As)
            E_bands = np.array(E_bands)
            bs = np.array(bs)
            bandgapfits = np.array(bandgapfits)

            # As_bs_pcov = np.array(As_bs_pcov)
            # As_E_bands_pcov = np.array(As_E_bands_pcov)

            # As_smooth = np.array(As_smooth)
            # E_bands_smooth = np.array(E_bands_smooth)
            # bs_smooth = np.array(bs_smooth)
            # bandgapfits_smooth = np.array(bandgapfits_smooth)

            range1list = np.array(range1list)
            range2list = np.array(range2list)
            i_succes = np.array(i_succes)

            # %%
            import random

            fig2, ax2 = plt.subplots(dpi=200)
            ax2.set_title(title_specimen + r"$\rm{-\;Bandgap\;Fit\;pixel[%d,%d]}$" % (pixx, pixy))
            ax2.set_xlabel(r"$\rm{Energy\;Loss\;[eV]\;}$")
            ax2.set_ylabel(r"$\rm{Intensity\;[a.u.]\;}$")
            ax2.set_ylim(-2, 400)
            ax2.set_xlim(0, dE2 +1)

            # fig3, ax3 = plt.subplots(dpi=200)
            # ax3.set_ylim(-2, 40)
            # ax3.set_xlim(.40, 5)

            # subtracted spectrum band
            ax2.fill_between(im.deltaE, np.nanpercentile(IEELSs_p_smooth, 16, axis=0),
                             np.nanpercentile(IEELSs_p_smooth, 84, axis=0), alpha=0.1, color='C0')
            # subtract spectrum median
            ax2.plot(im.deltaE, np.nanpercentile(IEELSs_p_smooth, 50, axis=0), alpha=0.5, color='C0', label=r"$\rm{Median\;subtracted\;spectra}$")

            #ax2.fill_between(im.deltaE[1:], np.nanpercentile(IEELSs_p_1d_smooth, 16, axis = 0), np.nanpercentile(IEELSs_p_1d_smooth, 84, axis = 0), alpha = 0.1, color = 'C1')
            #ax2.fill_between(im.deltaE[1:-1], np.nanpercentile(IEELSs_p_2d_smooth, 16, axis = 0), np.nanpercentile(IEELSs_p_2d_smooth, 84, axis = 0), alpha = 0.1, color = 'C2')

            #ax2.plot(im.deltaE[1:], np.nanpercentile(IEELSs_p_1d_smooth, 50, axis = 0), alpha = 0.5, color = 'C1')
            #ax2.plot(im.deltaE[1:-1], np.nanpercentile(IEELSs_p_2d_smooth, 50, axis = 0), alpha = 0.5, color = 'C2')
            ax2.axhline(0, color='black', alpha=0.5)
            ax2.axvspan(xmin=range1, xmax=range2, ymin=-1000, ymax=1000, color = 'C3', alpha=0.1)

            for k in range(1):
                r = random.random()
                g = random.random()
                b = random.random()
                color = 'C1'  # (r ,g ,b)
                bg_idx = np.random.randint(0, len(i_succes))

                # bandgap fit single model
                ax2.plot(im.deltaE, bandgapfits[bg_idx], color=color, label=r"$\rm{Fit\;single\;model}$")

                # subtracted spectrum
                ax2.plot(im.deltaE, IEELSs_p[i_succes[bg_idx]], color=color, alpha=0.2)

                # subtracted spectrum (smoothened)
                ax2.plot(im.deltaE, IEELSs_p_smooth[i_succes[bg_idx]], color=color, alpha=0.5)

                ax2.text(x=0.5, y=350, s=r"$\rm{Amp\;=\;%.2f\;}$" % (As[bg_idx]))
                ax2.text(x=0.5, y=320, s=r"$\rm{E_\mathrm{bg}\;=\;%.2f\;eV}$" % (E_bands[bg_idx]))
                ax2.text(x=0.5,y=290,s=r"$\rm{b\;=\;%.2f}$"%(bs[bg_idx]))
                print(bg_idx)
                # print("Amplitude to b variance:", As_bs_pcov[bg_idx])
                # print("Amplitude to bandgap variance:", As_E_bands_pcov[bg_idx])
                # ax2.plot(im.deltaE, bandgapfits,label = "raw", alpha = 1.0)
                # ax2.plot(im.deltaE, bandgapfits_smooth,label = "smooth")

                #ax3.plot(im.deltaE, IEELSs_p[i_succes[bg_idx]], alpha=0.3, color='C0')
                # ax3.plot(im.deltaE[1:], IEELSs_p_1d[i_succes[bg_idx]], alpha = 0.3, color='C1')
                # ax3.plot(im.deltaE[1:-1], IEELSs_p_2d[i_succes[bg_idx]], alpha = 0.4, color='C2')
                #
                # #ax3.plot(im.deltaE, IEELSs_p_smooth[i_succes[bg_idx]], color='C0')
                # ax3.plot(im.deltaE, np.nanpercentile(IEELSs_p_smooth, 50, axis=0))
                # ax3.fill_between(im.deltaE, np.nanpercentile(IEELSs_p_smooth, 84, axis=0),  np.nanpercentile(IEELSs_p_smooth, 16, axis=0), alpha = 0.3)
                #
                # ax3.plot(im.deltaE[1:], np.nanpercentile(IEELSs_p_1d_smooth, 50, axis=0))
                # ax3.fill_between(im.deltaE[1:], np.nanpercentile(IEELSs_p_1d_smooth, 84, axis=0),
                #                  np.nanpercentile(IEELSs_p_1d_smooth, 16, axis=0), alpha=0.3)
                #
                # ax3.plot(im.deltaE[1:-1], np.nanpercentile(IEELSs_p_2d_smooth, 50, axis=0))
                # ax3.fill_between(im.deltaE[1:-1], np.nanpercentile(IEELSs_p_2d_smooth, 84, axis=0),
                #                  np.nanpercentile(IEELSs_p_2d_smooth, 16, axis=0), alpha=0.3)
                #
                # # ax3.plot(im.deltaE[1:], IEELSs_p_1d_smooth[i_succes[bg_idx]], color='C1')
                # # ax3.plot(im.deltaE[1:-1], IEELSs_p_2d_smooth[i_succes[bg_idx]], color='C2')
                # fig3.savefig(os.path.join(im.output_path, 'bandgap_fit_der.pdf'))


            # bandgap fits band
            ax2.fill_between(im.deltaE, np.nanpercentile(bandgapfits, 16, axis=0),
                             np.nanpercentile(bandgapfits, 84, axis=0), alpha=0.1, color='C4')

            # ax2.axvline(range1, 0, 1, color='C3', linestyle='--')
            # ax2.axvline(range2, 0, 1, color='C3', linestyle='--')

            # ax2.fill_between(im.deltaE,
            #                 bandgap_test(im.deltaE, np.nanpercentile(As, 16, axis = 0),np.nanpercentile(E_bands, 16, axis = 0),np.nanpercentile(bs, 16, axis = 0)),
            #                 bandgap_test(im.deltaE, np.nanpercentile(As, 84, axis = 0),np.nanpercentile(E_bands, 84, axis = 0),np.nanpercentile(bs, 84, axis = 0)),
            #                 alpha = 0.2, color = 'C5')
            # ax2.fill_between(im.deltaE, np.nanpercentile(bandgapfits_smooth, 16, axis = 0), np.nanpercentile(bandgapfits_smooth, 84, axis = 0), alpha = 0.2, color = 'C5')
            # ax2.plot(im.deltaE, np.nanpercentile(bandgapfits, 50, axis = 0),label = "median bandgapfits", alpha = 1.0, color = 'C4')
            # ax2.plot(im.deltaE, np.nanpercentile(bandgapfits_smooth, 50, axis = 0),label = "smooth", color = 'C5')


            ax2.plot(im.deltaE, bandgap_test(im.deltaE, np.nanpercentile(As, 50, axis = 0),np.nanpercentile(E_bands, 50, axis = 0),np.nanpercentile(bs, 50, axis = 0)),label = r"$\rm{Fit\;median\;parameters}$", alpha = 1.0, color = 'C2', linestyle='dashed')
            # ax2.plot(im.deltaE,
            #          bandgap_test(im.deltaE, np.nanpercentile(As, 50, axis=0), np.nanpercentile(E_bands, 50, axis=0)),
            #          label=r"$\rm{median\;parameters}$", alpha=1.0, color='C4')
            # ax2.plot(im.deltaE, bandgap_test(im.deltaE, np.nanpercentile(As_smooth, 50, axis = 0),np.nanpercentile(E_bands_smooth, 50, axis = 0),np.nanpercentile(bs_smooth, 50, axis = 0)),label = "smooth", color = 'C5')
            ax2.legend(loc="lower right", frameon=False)
            fig2.savefig(os.path.join(im.output_path, 'bandgap_fit.pdf'))