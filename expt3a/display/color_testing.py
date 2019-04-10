from __future__ import division
import os, glob, sys, math, itertools
import numpy as np
from scipy.spatial.distance import pdist
import helper_functions_sustAttnWM as hf
from psychopy import visual, core, event, tools, misc
import psychopy.tools.colorspacetools as cst

l = 74
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

rgb = np.tile(rgb_circlepts,(n,1,1))
mask = np.zeros([100,1])
mask[-10:] = 1  # 10% of the radius is 1 (visible)
colortexrgb = rgb


win = visual.Window(size = (1200,1200),monitor='Dirk VU',fullscr = False, color=0, units='deg')

colorcirc = visual.RadialStim(win, tex=rgb, mask = mask,size=(4+.25)*2,ori=0, angularRes=256, angularCycles=1, interpolate=True)

colorcirc.draw()
circle = visual.Circle(win, radius = 1, edges=32, lineColor=None, fillColor = rgb_circlepts[0], fillColorSpace='rgb')
circle.draw()
win.flip()
core.wait(2)

colorcirc.draw()
circle = visual.Circle(win, radius = 1, edges=32, lineColor=None, fillColor = rgb_circlepts[100], fillColorSpace='rgb')
circle.draw()
win.flip()
core.wait(2)

colorcirc.draw()
circle = visual.Circle(win, radius = 1, edges=32, lineColor=None, fillColor = rgb_circlepts[200], fillColorSpace='rgb')
circle.draw()
win.flip()
core.wait(2)

colorcirc.draw()
circle = visual.Circle(win, radius = 1, edges=32, lineColor=None, fillColor = rgb_circlepts[300], fillColorSpace='rgb')
circle.draw()
win.flip()
core.wait(2)

colorcirc.draw()
circle = visual.Circle(win, radius = 1, edges=32, lineColor=None, fillColor = rgb_circlepts[400], fillColorSpace='rgb')
circle.draw()
win.flip()
win.flip()
core.wait(2)