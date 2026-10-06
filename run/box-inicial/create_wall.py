# creates the wall particles (floor + four side walls) of an open-top box
# by sfair (280926.1659)

# usage: python create_wall.py [-d D] [-L L] [-H HEIGHT]
#                              [-m MATID] [-n LAYERS] [-r RHO] [-o OUTPUT]
# output: x y z vx vy vz mass rho e matId S(9), all v, e, S zero
#   join with the sand: cat sand.0000 wall.0000 > box.0000
#
# box centered at x = y = 0, side = 2L (inner walls at x, y = +-L),
# floor at z = 0
# LAYERS*D must be at least sml
# inside, x and y use d_in = 2L/round(2L/D) so the lattice fits both walls;
# the sand should use x, y = -L + (i+1/2) d_in, z = (k+1/2) D

import argparse
import numpy as np

##################################################################
# PARAMETERS (defaults, can be changed in the command line)
D = 0.00805995977008 # particle distance [m]
L = 0.151            # half of the box side (side = 2L) [m]
HEIGHT = 0.25        # wall height [m]
MATID = 2            # wall material ID
LAYERS = 4           # wall thickness in particles
RHO = 2200.0         # density [kg/m^3], same as rho_0 in wall.cfg
OUTPUT = 'wall.0000'

########### ------------------------------------------------
########### ------------------------------------------------
###########
# THE CODE

def horizontal_axis(L, d, layers):
    # positions and spacing along x (or y)
    n_in = int(round(2*L/d))
    d_in = 2*L/n_in
    inner = -L + (np.arange(n_in) + 0.5)*d_in
    outer = L + (np.arange(layers) + 0.5)*d
    coords = np.concatenate((-outer[::-1], inner, outer))
    spacing = np.where(np.abs(coords) > L, d, d_in)
    return coords, spacing, d_in


parser = argparse.ArgumentParser(
    description='wall particles of an open-top box for miluphcuda')
parser.add_argument('-d', type=float, default=D)
parser.add_argument('-L', type=float, default=L)
parser.add_argument('-H', '--height', type=float, default=HEIGHT)
parser.add_argument('-m', '--matid', type=int, default=MATID)
parser.add_argument('-n', '--layers', type=int, default=LAYERS,
                    help='layers*d must be at least sml')
parser.add_argument('-r', '--rho', type=float, default=RHO)
parser.add_argument('-o', '--output', default=OUTPUT)
args = parser.parse_args()

###########
# lattice of the whole box, keep the wall points
x, dx, d_in = horizontal_axis(args.L, args.d, args.layers)
z = (np.arange(-args.layers, int(args.height/args.d)) + 0.5)*args.d

X, Y, Z = np.meshgrid(x, x, z, indexing='ij')
DX, DY, _ = np.meshgrid(dx, dx, z, indexing='ij')
wall = (np.abs(X) > args.L) | (np.abs(Y) > args.L) | (Z < 0)

n_wall = np.count_nonzero(wall)
zeros = np.zeros(n_wall)
mass = args.rho*DX[wall]*DY[wall]*args.d

###########
# x y z vx vy vz mass rho e matId S
data = np.column_stack([X[wall], Y[wall], Z[wall], zeros, zeros, zeros,
                        mass, np.full(n_wall, args.rho), zeros,
                        np.full(n_wall, args.matid)] + [zeros]*9)
np.savetxt(args.output, data, fmt=['%e']*9 + ['%d'] + ['%e']*9,
           delimiter='\t')

print("wall particles         : %d" % n_wall)
print("d inside (x, y)        : %.6f m" % d_in)
print("wall thickness         : %.4f m (must be >= sml in material.cfg)"
      % (args.layers*args.d))
