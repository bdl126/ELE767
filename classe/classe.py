import numpy as np
import random

class reseaux():
	#constructeur du réseau
	#on doit lui passer la config
	def __init__(self,configOriginal):

		self.config = configOriginal

		#initialise les matrices de poids de liens entre -0.1 et 0.1
		i=0
		self.lay = []
		self.lay.append(np.random.uniform(-0.1,0.1,(self.config["nbTrames"]*26, self.config["neuroneEntree"])))
		if self.config["nombreCoucheCachees"] > 0:
			self.lay.append(np.random.uniform(-0.1,0.1,(self.config["neuroneEntree"], self.config["neuroneCacher"][i])))
			i+=1
			while i <= self.config["nombreCoucheCachees"]-1:
				self.lay.append(np.random.uniform(-0.1,0.1,(self.config["neuroneCacher"][i-1], self.config["neuroneCacher"][i])))
				i+=1
			self.lay.append(np.random.uniform(-0.1,0.1,(self.config["neuroneCacher"][i-1], self.config["neuroneSortie"])))
		else:
			self.lay.append(np.random.uniform(-0.1, 0.1, (self.config["neuroneEntree"], self.config["neuroneSortie"])))

		#on met la constante de momentum à 0.5
		self.momentum = 0.5
		self.omegasDeltasPrec = []

	#retourne la valeur d'activation des neurones avant d'appliquer la fonction d'activation
	def activation(self,inputs,arrayPoids):
		return np.dot(inputs,arrayPoids)

	#retourne la sortie obtenue d'un set de donnée en entrée
	def test(self, input):
		#Activation
		activations=[]
		sortieFuncActivation = []
		activations.append(self.activation(input,self.lay[0]))
		sortieFuncActivation.append(self.config["foncActi"](activations[0]))
		for i in range(self.config["nombreCoucheCachees"]+1):
			activations.append(self.activation(sortieFuncActivation[i],self.lay[i+1]))
			sortieFuncActivation.append(self.config["foncActi"](activations[i+1]))
		
		return sortieFuncActivation[-1] #output obtenue

	#le réseau apprend selon un set de données d'entrée
	#on peut choisir d'appliquer le momentum ou non
	def train(self, input, outputDesire, momentum=False):
		
		#Activation
		activations=[]
		sortieFuncActivation = []
		activations.append(self.activation(input,self.lay[0]))
		sortieFuncActivation.append(self.config["foncActi"](activations[0]))
		for i in range(self.config["nombreCoucheCachees"]+1):
			activations.append(self.activation(sortieFuncActivation[i],self.lay[i+1]))
			sortieFuncActivation.append(self.config["foncActi"](activations[i+1]))
		
		#Signal d'erreur (Calcul des deltas d'erreur)
		if self.config["fonctionActivation"] == "sigmoid":
			deltas=[]
			deltas.insert(0,(outputDesire - sortieFuncActivation[-1])*self.config["foncActi"](sortieFuncActivation[-1],deriv=True))
			for i in range(self.config["nombreCoucheCachees"]+1):
				deltas.insert(0,np.matmul(deltas[-1-i],self.lay[-1-i].T)*self.config["foncActi"](sortieFuncActivation[-2-i],deriv=True)) 

		else:
			deltas=[]
			deltas.insert(0,(outputDesire - sortieFuncActivation[-1])*self.config["foncActi"](activations[-1],deriv=True))
			for i in range(self.config["nombreCoucheCachees"]+1):
				deltas.insert(0,np.matmul(deltas[-1-i],self.lay[-1-i].T)*self.config["foncActi"](activations[-2-i],deriv=True))

		#Correction sans momentum
		if momentum is False:
			omegasDeltas = []
			omegasDeltas.append(self.config["tauxApprentissage"]*np.outer(input, deltas[0]))
			for i in range(self.config["nombreCoucheCachees"]+1):
				omegasDeltas.append(self.config["tauxApprentissage"]*np.outer(sortieFuncActivation[i], deltas[i+1]))

		#Correction avec momentum
		else:
			if len(self.omegasDeltasPrec) > 0:
				omegasDeltas = []
				omegasDeltas.append(self.config["tauxApprentissage"] * np.outer(input, deltas[0]))
				for i in range(self.config["nombreCoucheCachees"] + 1):
					omegasDeltas.append(self.config["tauxApprentissage"] * np.outer(sortieFuncActivation[i], deltas[i + 1]))
				for i in range(len(omegasDeltas)):
					omegasDeltas[i]+=self.momentum * self.omegasDeltasPrec[i]
			else:
				omegasDeltas = []
				omegasDeltas.append(self.config["tauxApprentissage"] * np.outer(input, deltas[0]))
				for i in range(self.config["nombreCoucheCachees"] + 1):
					omegasDeltas.append(self.config["tauxApprentissage"] * np.outer(sortieFuncActivation[i], deltas[i + 1]))

		#actualisation
		for i in range(self.config["nombreCoucheCachees"]+1):
			self.lay[i] += omegasDeltas[i]


		self.omegasDeltasPrec = omegasDeltas

		return sortieFuncActivation[-1] #output obtenue
