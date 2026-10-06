
# -------------------------------------------------------
# import stuff
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

PLOT = 1

#distance of objects e angulo do giro
offset = (1737400*1.5)+0000 #metros
theta = np.radians(18) #graus para radianos

#Data name
file = f'small.0000'

#information
N = 90000
dens1 = 2.86e3  #gramas/cm³
dens2 = 0.91e3  #gramas/cm³
Rmax = 1737400 #metros

print("Starting...")

dx = int(Rmax*np.cbrt(4*np.pi)*np.cbrt(1/(3*N)))
N = (4*np.pi)/(3*(dx/Rmax)**3)
mass1 = 7.346e22 /N #kg
mass2 = 0.3*7.346e22 /N #kg
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
                pz.append(aux_z)
                vx.append(0)
                vy.append(0)
                vz.append(0)
                mat_type.append(0)
                dens.append(dens1)
                mass.append(mass1)

for i in x:
    for j in y:
        for k in z:
            Rsq = i**2 + j**2 + k**2
            if Rsq <= np.power(Rmax*0.3,2):
                
                px.append(i+offset)
                py.append(j+(offset*0.55))
                pz.append(k)                
                vx.append(-10000.)
                vy.append(-500.)
                vz.append(0.)
                mat_type.append(1)
                dens.append(dens2)
                mass.append(mass2)

# Cria um DataFrame combinando os vetores
# X, Y, Z, Vx, Vy, Vz, mass, density, energy, material type, sigma[0][0], sigma[0][1], sigma[0][2], sigma[1][0], sigma[1][1], sigma[1][2], sigma[2][0], sigma[2][1], sigma[2][2]
df = pd.DataFrame({'Coluna1': px, 'Coluna2': py, 'Coluna3': pz, 'Coluna4': vx, 'Coluna5': vy, 'Coluna6': vz, 'Coluna7': mass, 'Coluna8': dens, 'Coluna9': energy, 'Coluna10': mat_type, 'Coluna11': sigma[0][0], 'Coluna12': sigma[0][1], 'Coluna13': sigma[0][2], 'Coluna14': sigma[1][0], 'Coluna15': sigma[1][1], 'Coluna16': sigma[1][2], 'Coluna17': sigma[2][0], 'Coluna18': sigma[2][1], 'Coluna19': sigma[2][2]})             
df.to_csv(file, sep='\t',header=None, index=False, float_format="%.3f")

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
	fig.savefig("Teste_11.png", dpi=300)

	fig, ax = plt.subplots()

	ax.scatter(px, py, s=2, c='b')
	#ax.set_xlim(-1.4,3.6)
	#ax.set_ylim(-1.5,1.5)
	ax.set_xlabel("x")
	ax.set_ylabel("y")
	plt.grid()
	ax.set_aspect('equal')
	fig.savefig("Teste_12.png", dpi=300)
