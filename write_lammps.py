import numpy as np


def get_h2o(r):
    alpha=np.random.rand()*np.pi
    betta=np.random.rand()*2*np.pi
    data_molec=[]
    data_molec.append([2, r])# первый h
    h=0.9568 #bohr
    theta = 104.45/360.0*2.0*np.pi
    z_h1=h*np.sin(alpha)
    x_h1=h*np.cos(alpha)*np.cos(betta)
    y_h1=h*np.cos(alpha)*np.sin(betta)
    r_h1=np.array([x_h1,y_h1,z_h1])
    data_molec.append([1, r+r_h1])# первый h
    #theta = np.pi/2
    R = h*np.sin(theta) 
    t = np.random.rand()*2*np.pi
    #print(t)
    x_h2 = x_h1*np.cos(theta) + R/(x_h1**2 + z_h1**2)**0.5*(z_h1*np.cos(t) - x_h1*y_h1*np.sin(t)/(x_h1**2 + y_h1**2 + z_h1**2)**0.5)
    y_h2 = y_h1*np.cos(theta) + R*(x_h1**2 + z_h1**2)**0.5*np.sin(t)/(x_h1**2 + y_h1**2 + z_h1**2)**0.5
    z_h2 = z_h1*np.cos(theta) - R/(x_h1**2 + z_h1**2)**0.5*(x_h1*np.cos(t) + z_h1*y_h1*np.sin(t)/(x_h1**2 + y_h1**2 + z_h1**2)**0.5)
    r_h2=np.array([x_h2,y_h2,z_h2])
    data_molec.append([1, r+r_h2])# первый h
    
    #print(np.arccos(np.dot(r_h1,r_h2)/np.linalg.norm(r_h1)/np.linalg.norm(r_h2))/np.pi*180 )
    #print(np.dot(r_h1,r_h2)/np.linalg.norm(r_h1)/np.linalg.norm(r_h2))
    return data_molec

def get_structure(box_length, N_O):
    data = []
    i = 0
    particle_num = N_O
    ind = np.hstack([np.zeros(particle_num) + 1,(np.zeros(35937 - particle_num))])
    print(len(ind))
    np.random.shuffle(ind)
   	#assuming there are 1000 O
    for x_i in np.linspace(0.1*box_length, 0.9*box_length, 33): #int(particle_num**(1.0/3.0))
        for y_i in np.linspace(0.1*box_length, 0.9*box_length,33):
            for z_i in np.linspace(0.1*box_length, 0.9*box_length, 33):  
                if ind[i]==1:
                	#print('dfbg')
                	r = np.array([x_i + np.random.rand()*0.01*box_length, y_i+ np.random.rand()*0.01*box_length, z_i+ np.random.rand()*0.01*box_length])
                	data.append(get_h2o(r))
                i = i + 1
    print(i)
    return data


def write_lammps_data(filename, box_length, N_O):
	N_particles=N_O*3
	print ("Generate Structure for box={:f} and {:d} H2O".format(box_length,N_O))
	data=get_structure(box_length,N_O)
	N_bonds = int(N_particles*(2/3))
	N_angles = int(N_particles/3)
	with open(filename,"w") as f:
		f.write("Created by Egor Agapov for water research\n"+
				"\n"+
				"{:d} atoms\n".format(N_particles)+ 
				"{:d} bonds\n".format(N_bonds)+ 
				"{:d} angles\n".format(N_angles)+ 
				"2 atom types\n" +
				"1 bond types\n" +
				"1 angle types\n" +
				"\n"+
				"0.000000 {:.6f} xlo xhi\n".format(box_length)+
				"0.000000 {:.6f} ylo yhi\n".format(box_length)+
				"0.000000 {:.6f} zlo zhi\n".format(box_length)+
				"\n" +
				"Masses\n"+
				"\n"+
				"1 1.00794\n"+
				"2 15.9994\n"+
				"\n"+
				"Atoms\n"+
				"\n")
		print("Write coordinates")
		k = 0
		for i in range(N_O):
			molec=data[i]
			#print(molec)
			for atom in molec:
				if atom[0]==1:
					atom_type=1
					q=0.52
					r=atom[1]
				else:
					atom_type=2
					q=-1.04
					r=atom[1]
				k +=1
				f.write("{:d}\t{:d}\t{:d}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\n".format(k, i+1, atom_type, q, r[0], r[1], r[2]))
		
		f.write("\nBonds\n"+ "\n")
		k = 0
		i = 0
		bond_type = 1

		for i in range(N_O):
			molec=data[i]
			k +=3
			i +=1
			f.write("{:d}\t{:d}\t{:d}\t{:d}\n".format(i, bond_type, k-2, k)) 
			f.write("{:d}\t{:d}\t{:d}\t{:d}\n".format(i+1, bond_type, k-2, k-1))

		with open("bonds.txt","w") as g:
			k = 0
			i = 0
			bond_type = 1

			for i in range(N_O):
				molec=data[i]
				k +=3
				i +=1
				g.write("{:d}\t{:d}\n".format(k-2, k)) 
				g.write("{:d}\t{:d}\n".format(k-2, k-1))


		f.write("\nAngles\n"+ "\n")
		k = 0
		i = 0
		angle_type = 1
		for i in range(N_O):
			molec=data[i]
			k +=3
			i +=1
			f.write("{:d}\t{:d}\t{:d}\t{:d}\t{:d}\n".format(i, angle_type, k-1, k-2, k)) 

		
box_length  = 50
with open("config.txt","r") as f:
	for line in f:
		box_length = float(line.split()[1])
print(box_length)

filename = 'data.water'
#box_length = 200
N_O = 20000


#Na=6.022e23
#a=(N_h2*2/Na/rho)**(1/3)*1e8/0.529 # bohr
#print ("rho={:f} g/cc, N_h2={:d} --> a={:f} Bohr".format(rho,N_h2,a))
write_lammps_data(filename, box_length, N_O=N_O)


# https://lammps.sandia.gov/doc/2001/data_format.html
