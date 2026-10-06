
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
file = f'queda.0000'

#information
N = 1000
dens1 = 2.86e3  #gramas/cm³
Rmax = 0.05 #metros

print("Starting...")

dx = float(Rmax*np.cbrt(4*np.pi)*np.cbrt(1/(3*N)))
N = (4*np.pi)/(3*(dx/Rmax)**3)
mass1 = 1.52 /N #kg
print("dx = ", dx)
print("N = ", N)

x = np.arange(-Rmax*1.6, (Rmax+dx)*1.6, dx)
y = np.arange(-Rmax*1.6, (Rmax+dx)*1.6, dx)
z = np.arange(-Rmax*1.6, (Rmax+dx)*1.6, dx)

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
            Rsq = i**2 + j**2 + k**2
            if Rsq < np.power(Rmax,2):
            
                # Matriz de rotação em Y
                aux_z = -(i*np.sin(theta)) + (k*np.cos(theta))     
                aux_x = (i*np.cos(theta)) + (k*np.sin(theta))
                
                # Matriz de rotação em Z
                aux_y = (aux_x*np.sin(theta)) + (j*np.cos(theta))     
                aux_x = (aux_x*np.cos(theta)) - (j*np.sin(theta))
                
                px.append(aux_x)
                py.append(aux_y)
                pz.append(aux_z+0.5)
                vx.append(0)
                vy.append(0)
                vz.append(-5)
                mat_type.append(1)
                dens.append(dens1)
                mass.append(mass1)


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
	fig.savefig("Queda_1.png", dpi=300)
	plt.show()

	fig, ax = plt.subplots()

	ax.scatter(px, pz, s=2, c='b')
	#ax.set_xlim(-1.4,3.6)
	#ax.set_ylim(-1.5,1.5)
	ax.set_xlabel("x")
	ax.set_ylabel("z")
	plt.grid()
	ax.set_aspect('equal')
	fig.savefig("Queda_2.png", dpi=300)
