# creates the wall particles of a silo: vertical cylinder with a conical
# funnel at the bottom, open at the top and at the outlet
# by sfair (051026.1700)

# usage: python create_silo.py [-d D] [-R R] [-Ro R_OUT] [-Hc H_CYL]
#                                [-Hf H_FUN] [-z Z0] [-m MATID] [-n LAYERS]
#                                [-r RHO] [-o OUTPUT]
# output: x y z vx vy vz mass rho e matId S(9), all v, e, S zero
#   join with the sand: cat sand.0000 silo.0000 > sand_silo.0000
#
# axis of the silo at x = y = 0, outlet at z = Z0, funnel from Z0 to
# Z0 + H_FUN, cylinder from Z0 + H_FUN to Z0 + H_FUN + H_CYL
# R, R_OUT, H_CYL and H_FUN are internal measurements, the wall particles
# are outside them, up to the radius R + LAYERS*D at all heights (the
# outside of the silo is a cylinder, the wall is thicker around the funnel)
# LAYERS*D must be at least sml
# the sand should use x, y = (i+1/2) D, z = Z0 + (k+1/2) D

import argparse
import numpy as np

##################################################################
# PARAMETERS (defaults, can be changed in the command line)
D = 0.014            # particle distance [m]
R = 0.10             # inner radius of the cylinder [m]
R_OUT = 0.02         # inner radius of the outlet [m]
H_CYL = 0.30         # height of the cylinder [m]
H_FUN = 0.08         # height of the funnel [m]
Z0 = 0.0             # height of the outlet [m]
MATID = 1            # wall material ID
LAYERS = 4           # wall thickness of the cylinder in particles
RHO = 2200.0         # density [kg/m^3], same as rho_0 in wall.cfg
OUTPUT = 'silo.0000'

########### ------------------------------------------------
########### ------------------------------------------------
###########
# THE CODE

def inner_radius(z, r, r_out, h_fun):
    # inner radius of the silo at the height z above the outlet
    return np.where(z < h_fun, r_out + (r - r_out)*z/h_fun, r)


parser = argparse.ArgumentParser(
    description='wall particles of a silo with a funnel for miluphcuda')
parser.add_argument('-d', type=float, default=D)
parser.add_argument('-R', type=float, default=R)
parser.add_argument('-Ro', '--r_out', type=float, default=R_OUT)
parser.add_argument('-Hc', '--h_cyl', type=float, default=H_CYL)
parser.add_argument('-Hf', '--h_fun', type=float, default=H_FUN)
parser.add_argument('-z', '--z0', type=float, default=Z0)
parser.add_argument('-m', '--matid', type=int, default=MATID)
parser.add_argument('-n', '--layers', type=int, default=LAYERS,
                    help='layers*d must be at least sml')
parser.add_argument('-r', '--rho', type=float, default=RHO)
parser.add_argument('-o', '--output', default=OUTPUT)
args = parser.parse_args()

###########
# lattice around the whole silo, keep the wall points
thickness = args.layers*args.d
height = args.h_fun + args.h_cyl

n = int(np.ceil((args.R + thickness)/args.d))
x = (np.arange(-n, n) + 0.5)*args.d
z = (np.arange(int(np.ceil(height/args.d))) + 0.5)*args.d  # above the outlet

X, Y, Z = np.meshgrid(x, x, z, indexing='ij')
RAD = np.hypot(X, Y)

wall = (RAD > inner_radius(Z, args.R, args.r_out, args.h_fun)) \
    & (RAD <= args.R + thickness) & (Z < height)

n_wall = np.count_nonzero(wall)
zeros = np.zeros(n_wall)
mass = np.full(n_wall, args.rho*args.d**3)

###########
# x y z vx vy vz mass rho e matId S
data = np.column_stack([X[wall], Y[wall], Z[wall] + args.z0,
                        zeros, zeros, zeros,
                        mass, np.full(n_wall, args.rho), zeros,
                        np.full(n_wall, args.matid)] + [zeros]*9)
np.savetxt(args.output, data, fmt=['%e']*9 + ['%d'] + ['%e']*9,
           delimiter='\t')

print("wall particles         : %d" % n_wall)
print("wall thickness         : %.4f m (must be >= sml in material.cfg)"
      % thickness)
print("outlet diameter        : %.4f m (%.1f particles)"
      % (2*args.r_out, 2*args.r_out/args.d))
