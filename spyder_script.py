#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 22:34:02 2022

@author: ejdrup
"""

import numpy as np
import glob
import matplotlib.pyplot as plt

def convert_signal(signal_ch,isosbestic,s_fit,e_fit):
    '''
    This function has four parameters
    signal:        Signal channel
    isosbestic:    Isosbestic channel
    s_fit:  Where to start the linear fit 
    e_fit:    Where to terminate the fit 
    
    Make sure to trim the signal and isosbestic to the same length using [:-1] (or -2, etc.)
    '''

    p = np.polyfit(isosbestic[:e_fit], signal_ch[:e_fit], 1)
    isos_fit = p[0]*isosbestic+p[1]
    
    dFF = (signal_ch-isos_fit)/isos_fit
    z_scored = (dFF-np.mean(dFF[s_fit:e_fit]))\
    /np.std(dFF[s_fit:e_fit])
    
    return z_scored

#%% Load data

# Load photometry file names
files_photometry_amph = np.sort(glob.glob("data/fiber photometry/*amph*"))
files_photometry_ctrl = np.sort(glob.glob("data/fiber photometry/*ctrl*"))

# Load photometry files
data_photometry_amph = []
data_photometry_ctrl = []
for i in range(len(files_photometry_amph)):
    data_photometry_amph.append(np.genfromtxt(files_photometry_amph[i],delimiter=" "))
    data_photometry_ctrl.append(np.genfromtxt(files_photometry_ctrl[i],delimiter=" "))
    
# Load microdialysis files
data_microdialysis_amph = np.genfromtxt("data/microdialysis/mice_amph.txt",delimiter=" ")
data_microdialysis_ctrl = np.genfromtxt("data/microdialysis/mice_ctrl.txt",delimiter=" ")

#%% Preprocess


# Convert the raw using the convert_signal function
# Z-score is fitted to the twenty minutes leading up to injection
# The 45 minutes leading up to and 100 minutes after injection are isolated
zF_amph = np.zeros((7,20*60*145))
zF_ctrl = np.zeros((7,20*60*145))
for i in range(len(files_photometry_amph)):
    
    # Mice are injected at index 80000
    inj_idx = 80000
    
    # Vehicle/ctrl
    zF_ctrl[i,:] = convert_signal(data_photometry_ctrl[i][1,:],
                   data_photometry_ctrl[i][0,:],
                   inj_idx-20*60*20,inj_idx)[inj_idx-20*60*45:inj_idx+20*60*100]
    
    # For mouse 5 and 6 receiving amphetamine, the recording was interrupted early and restarted
    if i > 4:
        inj_idx = 55000
    
    # Amphetamine
    zF_amph[i,:] = convert_signal(data_photometry_amph[i][1,:],
                   data_photometry_amph[i][0,:],
                   inj_idx-20*60*20,inj_idx)[inj_idx-20*60*45:inj_idx+20*60*100]

    
#%% Plot zF traces

# Initiate axes
fig, (ax1, ax2) = plt.subplots(1,2,figsize = (6,4), dpi = 400)

# Convert indecies to minutes
time = np.linspace(-45,100,20*60*145)

# Plot vehicle traces
for i in range(len(zF_ctrl)):
    ax1.plot(time, zF_ctrl[i,:]+i*30, color = "dimgrey")

# Plot amphetamine traces
for i in range(len(zF_amph)):
    ax2.plot(time, zF_amph[i,:]+i*30, color = "cornflowerblue")
    
# Plot y-scale bar
ax1.plot([120,120], [80,100], color = "k", clip_on = False)
ax1.text(118, 90, "20 zF", ha = "right", va = "center", rotation = 90)

# Adjust axes
ax1.set_title("Vehicle traces", fontsize = 10)
ax1.set_xlabel("Minutes from vehicle injection")
ax1.set_xlim(-50,100)
ax1.set_yticks([])
ax1.set_ylim(-10,200)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)

ax2.set_title("Amphetamine traces", fontsize = 10)
ax2.set_xlabel("Minutes from amph. injection")
ax2.set_xlim(-50,100)
ax2.set_yticks([])
ax2.set_ylim(-10,200)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
    
#%% Plot microdialysis

# Initiate axes
fig, (ax1, ax2) = plt.subplots(1,2,figsize = (6,2), dpi = 400)

# Convert indecies to minutes
time = np.linspace(-60,120,10)

# Vehicle
ax1.plot(time, np.nanmean(data_microdialysis_ctrl/np.mean(data_microdialysis_ctrl[:4,:]), axis = 1), 
         color = "dimgrey", lw = 2, zorder = 10)
ax1.plot(time, data_microdialysis_ctrl/np.mean(data_microdialysis_ctrl[:4,:]),
         'o', ms = 3, color = "grey", clip_on = False, zorder = 1)

# Amphetamine
ax2.plot(time, np.nanmean(data_microdialysis_amph/np.mean(data_microdialysis_amph[:4,:]), axis = 1), 
         color = "cornflowerblue", lw = 2, zorder = 10)
ax2.plot(time, data_microdialysis_amph/np.mean(data_microdialysis_amph[:4,:]),
         'o', ms = 3, color = "grey", clip_on = False, zorder = 1)


# Adjust axes
ax1.set_title("Vehicle trace", fontsize = 10)
ax1.set_xlabel("Minutes from vehicle injection")
ax1.set_ylabel("Fold change\nfrom baseline")
ax1.set_xlim(-60,120)
ax1.set_xticks([-60,0,60,120])
ax1.set_ylim(-2,30)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax2.set_title("Amphetamine trace", fontsize = 10)
ax2.set_xlabel("Minutes from amph. injection")
ax2.set_xlim(-60,120)
ax2.set_xticks([-60,0,60,120])
ax2.set_ylim(-2,30)
ax2.set_yticks([])
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)

