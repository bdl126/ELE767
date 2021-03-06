import numpy as np
np.set_printoptions(threshold=1000000)

def sauvegardePoids(reseau,path):
	print("début de sauvegarde des poids")
	for i in range(int(reseau.config["nombreCoucheCachees"])+2):
		data = reseau.lay[i]
		# Write the array to disk
		with open(path+"/configPoidsLayer"+str(i)+".txt", 'w') as outfile:
			outfile.write('# Poids couche 1: {0}\n#Donnée 1\n'.format(data.shape))
			j = 2
			for data_slice in data:
				np.savetxt(outfile, data_slice, fmt='%-7.10f')
				outfile.write('# Donnée {}\n'.format(j))
				j+=1
		outfile.close()

	print("fin de sauvegarde des poids")

def chargerPoids(reseau,path):
	print("début de chargement des poids")
	# Read the array from disk
	for i in range(reseau.config["nombreCoucheCachees"]+2):
		new_data = np.loadtxt(path+"/configPoidsLayer"+str(i)+".txt")
		reseau.lay[i] = new_data.reshape(reseau.lay[i].shape)

	print("fin de chargement des poids")