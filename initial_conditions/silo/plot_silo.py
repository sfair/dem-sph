# plots the x y z positions of the silo particles (silo.0000) with the
# internal measurements on top: 3D view of the half y > 0 + three slices
# (x-z at the middle y, x-y at the middle of the cylinder, x-y at the outlet)
# by sfair (051026.1700)

# usage: python plot_silo.py [INPUT] [OUTPUT]
# input: miluphcuda particle file, x y z in the first 3 columns
# output: png with the plots

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##################################################################
# PARAMETERS (same as in create_silo.py)
INPUT = sys.argv[1] if len(sys.argv) > 1 else 'silo.0000'
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else 'silo.png'
R = 0.10             # inner radius of the cylinder [m]
R_OUT = 0.02         # inner radius of the outlet [m]
H_CYL = 0.30         # height of the cylinder [m]
H_FUN = 0.08         # height of the funnel [m]
Z0 = 0.0             # height of the outlet [m]

########### ------------------------------------------------
########### ------------------------------------------------
###########
# THE CODE

def nearest(values, target):
    # lattice value closest to target, to pick one layer of particles
    return values[(values - target).abs().idxmin()]


def inner_radius(z):
    # inner radius of the silo at the height z
    if z - Z0 < H_FUN:
        return R_OUT + (R - R_OUT)*(z - Z0)/H_FUN
    return R


def dimension(ax, p1, p2, text, **kwargs):
    # double arrow from p1 to p2 with the measurement
    ax.annotate('', xy=p1, xytext=p2,
                arrowprops=dict(arrowstyle='<->', color='0.3'))
    ax.annotate(text, xy=((p1[0] + p2[0])/2, (p1[1] + p2[1])/2),
                textcoords='offset points', color='0.3', **kwargs)


df = pd.read_table(INPUT, sep=r'\s+', header=None, usecols=[0, 1, 2],
                   names=['x', 'y', 'z'])

z_top = Z0 + H_FUN + H_CYL
z_cyl = nearest(df['z'], Z0 + H_FUN + H_CYL/2)
z_out = df['z'].min()

fig = plt.figure(figsize=(10, 10))

# 3D view, half of the silo to see the inside
df_temp = df.loc[df['y'] > 0]
ax = fig.add_subplot(2, 2, 1, projection='3d')
ax.scatter(df_temp['x'], df_temp['y'], df_temp['z'], s=3, c=df_temp['z'],
           depthshade=False)
ax.set_box_aspect(tuple(df_temp.max() - df_temp.min()))  # same scale
ax.set_title('y > 0')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('z [m]')

# x-z slice with the inner surface and the internal measurements
y_mid = nearest(df['y'], 0.0)
df_temp = df.loc[df['y'] == y_mid]
x_max = df_temp['x'].max()
ax = fig.add_subplot(2, 2, 2)
ax.plot(df_temp['x'], df_temp['z'], 'o', markersize=3)
for side in [-1, 1]:
    ax.plot([side*R_OUT, side*R, side*R], [Z0, Z0 + H_FUN, z_top], 'k-',
            linewidth=1)
dimension(ax, (-R, Z0 + H_FUN + 0.6*H_CYL), (R, Z0 + H_FUN + 0.6*H_CYL),
          '%g cm' % (200*R), xytext=(0, 5), ha='center')
dimension(ax, (-R_OUT, Z0 - 0.02), (R_OUT, Z0 - 0.02),
          '%g cm' % (200*R_OUT), xytext=(0, -14), ha='center')
dimension(ax, (x_max + 0.02, Z0 + H_FUN), (x_max + 0.02, z_top),
          '%g cm' % (100*H_CYL), xytext=(5, 0), va='center')
dimension(ax, (x_max + 0.02, Z0), (x_max + 0.02, Z0 + H_FUN),
          '%g cm' % (100*H_FUN), xytext=(5, 0), va='center')
ax.set_xlim(-x_max - 0.02, x_max + 0.08)
ax.set_ylim(Z0 - 0.05, z_top + 0.02)
ax.set_aspect('equal')
ax.set_title('y = %.4f m' % y_mid)
ax.set_xlabel('x [m]')
ax.set_ylabel('z [m]')

# x-y slices with the inner circle
angle = np.linspace(0, 2*np.pi, 200)
j = 3
for value, name in [(z_cyl, 'cylinder'), (z_out, 'outlet')]:
    df_temp = df.loc[df['z'] == value]
    radius = inner_radius(value)
    ax = fig.add_subplot(2, 2, j)
    ax.plot(df_temp['x'], df_temp['y'], 'o', markersize=3)
    ax.plot(radius*np.cos(angle), radius*np.sin(angle), 'k-', linewidth=1)
    dimension(ax, (-radius, 0), (radius, 0), '%.1f cm' % (200*radius),
              xytext=(0, 5), ha='center')
    ax.set_xlim(-x_max - 0.02, x_max + 0.02)
    ax.set_ylim(-x_max - 0.02, x_max + 0.02)
    ax.set_aspect('equal')
    ax.set_title('z = %.4f m (%s)' % (value, name))
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    j = j + 1

plt.tight_layout(w_pad=4)
plt.savefig(OUTPUT, facecolor='white', dpi='figure')
plt.show()
