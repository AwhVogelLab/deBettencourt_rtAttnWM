from __future__ import division
import os, glob, sys, math, itertools
import numpy as np
from scipy.spatial.distance import pdist
#import helper_functions_sustAttnWM as hf
from psychopy import visual, core, event, tools, misc
import psychopy.tools.colorspacetools as cst

win = visual.Window(size = (550,550),monitor='imac',fullscr = False, color=0, units='deg') 

# colortextureRes = 512
# colortexhsv = np.ones([colortextureRes,colortextureRes,3], dtype=float)
# colortexhsv[:,:,0] = np.linspace(0,360,colortextureRes, endpoint=False)
# colortexhsv[:,:,1] = 1
# colortexhsv[:,:,2] = 1
# rgb = misc.hsv2rgb(colortexhsv)
# mask = np.zeros([100,1])
# mask[-10:] = 1  # 10% of the radius is 1 (visible)
# colortexrgb = rgb
# colorcirc = visual.RadialStim(win, tex=rgb, mask = mask,size=(5+0.25)*2,ori=0, angularRes=256, angularCycles=1, interpolate=True)

l = 70
a = 20
b = 38
r = 60
n = 512
lab_circlepts = np.empty((n,2))
rgb_circlepts = np.empty((n,3))
for i in range(n):
    x = (a + r * np.sin(np.deg2rad(float(i)/n*360)))
    y = (b + r * np.cos(np.deg2rad(float(i)/n*360)))
    lab_circlepts[i] = [x,y]
    rgb_circlepts[i] = cst.cielab2rgb([l, x, y],transferFunc=cst.srgbTF,clip=True)


colortextureRes = 512
colortexhsv = np.ones([colortextureRes,colortextureRes,3], dtype=float)
colortexhsv[:,:,0] = np.linspace(0,colortextureRes,colortextureRes, endpoint=False)
colortexhsv[:,:,1] = 1
colortexhsv[:,:,2] = 1
rgb = misc.hsv2rgb(colortexhsv)
rgb = np.tile(rgb_circlepts,(colortextureRes,1,1))
mask = np.zeros([100,1])
mask[-10:] = 1  # 10% of the radius is 1 (visible)
colortexrgb = rgb

circrad = 4
circoffset = .25
colorcirc = visual.RadialStim(win, tex=rgb, mask = mask,size=(circrad+circoffset)*2,ori=0, angularRes=256, angularCycles=1, interpolate=True)        


colorcirc.draw()
#win.flip()
#core.wait(1)
win.getMovieFrame(buffer='back')
win.saveMovieFrames('colorwheel.png')
core.wait(1)