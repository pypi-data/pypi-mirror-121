#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

min_blue_saturation = 0*255

###############################################################################
# this function creates the color masks
# change it if the first pass is picking up the wrong colors
def createColorMasks(HSV, RGB):
#    whiteMask = LAB[...,0] > 70
#    redMask = (LAB[...,1] > 10) & (LAB[...,2] > 0) & np.logical_not(whiteMask)
#    blueMask = (LAB[...,2] < 0) & (LAB[...,1] < 15) & np.logical_not(whiteMask) & np.logical_not(redMask)

    whiteMask = (HSV[...,1] <= 0.06*255) & (HSV[...,2] >= 0.8*255)
    redMask = (0.78*255 < HSV[...,0]) & (HSV[...,0] < 1*255) & np.logical_not(whiteMask)
    blueMask = (0.69*255 < HSV[...,0]) & (HSV[...,0] < 0.72*255) & (HSV[...,1] >= min_blue_saturation) & np.logical_not(whiteMask)
    otherMask = np.logical_not(whiteMask|blueMask|redMask)

    return whiteMask, redMask, blueMask, otherMask

###############################################################################
# k neighbors classifier settings
## this is the second pass which attempts to classify pixes missed in the first
## pass into blue, red, or unidentifiable. It does not classify white, that is
## is done separately

#raw settings for KNeighborsClassifier
#see https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier
KNN : dict = {'n_neighbors':5, 'n_jobs':-1}

# dont classify points if the color is very different from red, blue or white
useWeights : bool = False
# number of standard deviations which makes a color very different
stdevMultiplier : float = 2

# minimum fraction of neighbors with the same label needed to classify a pixel
#default 1 or 100% of neighbors must be the same
min_consensus : float = 0.8

# fraction of the number of colored pixels
# this is used becase if all white values were taken it would take prohibitively
# long so instead a random sample of white values are added in
# increase this to decrease the variability in results
# should be greater than 0
frac_white : float = 0.25
frac_blue : float = 0.95
frac_red : float = 0.75

max_blue : int = 500000
max_red : int = 1000000

###############################################################################
# other settings

# show masks of the color filter results
show_firstPass = False

# save mask images to a directory
save_images = True

# show image plots
show_images = True
###############################################################################
