# plots the x y z positions of a particle file (e.g. wall.0000):
# 3D view + three slices (x-z at the middle y, y-z at the middle x,
# x-y at the middle height)
# by sfair (280926.1659)

# usage: python plot_wall.py [INPUT] [OUTPUT]
# input: miluphcuda particle file, x y z in the first 3 columns
# output: png with the plots

import sys
import pandas as pd
import matplotlib.pyplot as plt

##################################################################
# PARAMETERS
INPUT = sys.argv[1] if len(sys.argv) > 1 else 'wall.0000'
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else 'wall.png'

########### ------------------------------------------------
########### ------------------------------------------------
###########
# THE CODE

def nearest(values, target):
    # lattice value closest to target, to pick one layer of particles
    return values[(values - target).abs().idxmin()]


df = pd.read_table(INPUT, sep=r'\s+', header=None, usecols=[0, 1, 2],
                   names=['x', 'y', 'z'])

# (horizontal axis, vertical axis, cut axis, cut value)
slices = [('x', 'z', 'y', nearest(df['y'], 0.0)),
          ('y', 'z', 'x', nearest(df['x'], 0.0)),
          ('x', 'y', 'z', nearest(df['z'], df['z'].max()/2))]

fig = plt.figure(figsize=(10, 10))

# 3D view
ax = fig.add_subplot(2, 2, 1, projection='3d')
ax.scatter(df['x'], df['y'], df['z'], s=3, c=df['z'], depthshade=False)
ax.set_box_aspect(tuple(df.max() - df.min()))  # same scale on all axes
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('z [m]')

# slices
j = 2
for h, v, cut, value in slices:
    df_temp = df.loc[df[cut] == value]
    ax = fig.add_subplot(2, 2, j)
    ax.plot(df_temp[h], df_temp[v], 'o', markersize=3)
    ax.set_aspect('equal')
    ax.set_title('%s = %.4f m' % (cut, value))
    ax.set_xlabel('%s [m]' % h)
    ax.set_ylabel('%s [m]' % v)
    j = j + 1

plt.tight_layout(w_pad=4)
plt.savefig(OUTPUT, facecolor='white', dpi='figure')
plt.show()
