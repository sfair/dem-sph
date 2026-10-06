
# -------------------------------------------------------
# import stuff
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

PLOT = 1

#angulo do giro
theta = np.radians(18) #graus para radianos

#Data name
file = f'box.0000'

#information
#N = 25000
dens1 = 2.20e3  #gramas/cm³
Xmax = 0.15 #metros
Ymax = 0.15 #metros
Zmax = 0.2 #metros

print("Starting...")

dx = 0.008059959770082347

x = np.arange(-Xmax, (Xmax+dx), dx)
y = np.arange(-Ymax, (Ymax+dx), dx)
z = np.arange(0, (Zmax+dx), dx)

N = len(x) * len(y) * len(z)
mass1 = 26 /N #kg
print("dx = ", dx)
print("N = ", N)

#Matriz 3x3 de zeros
sigma = np.zeros((3, 3))

energy = 0.0

mass = []
dens = []
mat_type = []
px = []
py = []
pz = []
vx = []
vy = []
vz = []

for i in x:
    for j in y:
        for k in z:      
            px.append(i)
            py.append(j)
            pz.append(k+0.25)
            vx.append(0)
            vy.append(0)
            vz.append(0)
            mat_type.append(0)
            dens.append(dens1)
            mass.append(mass1)
            N = N+1

# Cria um DataFrame combinando os vetores
# X, Y, Z, Vx, Vy, Vz, mass, density, energy, material type, sigma[0][0], sigma[0][1], sigma[0][2], sigma[1][0], sigma[1][1], sigma[1][2], sigma[2][0], sigma[2][1], sigma[2][2]
df = pd.DataFrame({'Coluna1': px, 'Coluna2': py, 'Coluna3': pz, 'Coluna4': vx, 'Coluna5': vy, 'Coluna6': vz, 'Coluna7': mass, 'Coluna8': dens, 'Coluna9': energy, 'Coluna10': mat_type, 'Coluna11': sigma[0][0], 'Coluna12': sigma[0][1], 'Coluna13': sigma[0][2], 'Coluna14': sigma[1][0], 'Coluna15': sigma[1][1], 'Coluna16': sigma[1][2], 'Coluna17': sigma[2][0], 'Coluna18': sigma[2][1], 'Coluna19': sigma[2][2]})             
df.to_csv(file, sep='\t',header=None, index=False, float_format="%.4f")

if PLOT:
	plt.figure(figsize=(1,0.7))
		
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')

	ax.scatter(px, py, pz, c='b', marker='o', s = 5)
	ax.set_box_aspect([1, 1, 1])
	#ax.set_xlim(-2,3.5)
	#ax.set_ylim(-1.5,1.5)
	#ax.set_zlim(-2,2)
	ax.set_xlabel("x")
	ax.set_ylabel("y")
	ax.set_zlabel("z")
	plt.grid()
	fig.savefig("material_1.png", dpi=300)
	plt.show()

	fig, ax = plt.subplots()

	ax.scatter(px, pz, s=2, c='b')
	#ax.set_xlim(-1.4,3.6)
	#ax.set_ylim(-1.5,1.5)
	ax.set_xlabel("x")
	ax.set_ylabel("z")
	plt.grid()
	ax.set_aspect('equal')
	fig.savefig("material_2.png", dpi=300)
