#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:46:21 2020

@author: josephgross
"""


from mpl_toolkits import mplot3d

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(15,12))
ax = plt.axes(projection='3d')

# Data for a three-dimensional line
ax = fig.gca(projection='3d')


sampling_rate = 100
# Create our x, y and z coordinates.
t = np.arange(-4.0 * np.pi, 4.0 * np.pi, 0.1)
t = np.linspace(0, 2, 2*sampling_rate, endpoint=False)


y1 = np.zeros(t.size) + 1
z1 = 1 * np.sin(1 * 2 * np.pi * t)

y2 = np.zeros(t.size) + 2
z2 = 1 * np.sin(2 * 2 * np.pi * t)

y3 = np.zeros(t.size) + 3
z3 = 1 * np.sin(3 * 2 * np.pi * t)

y = np.zeros(t.size)
z = z1 + z2 + z3

# Create and show the plot.
ax.plot(t, y1, z1, "blue")
ax.plot(t, y2, z2, "green")
ax.plot(t, y3, z3, "red")
ax.plot(t, y, z, "black")


ax.set_xlabel("Time [s]", fontsize = 20)
ax.set_ylabel("Frequency [Hz]", fontsize = 20)
ax.set_zlabel("Amplitude",  fontsize = 20)

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
plt.show()

print(np.zeros(10) + 1)

