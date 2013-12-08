import snappy.snap as snap
from consolidateFeatures import *
import scipy.io as io
import numpy as np

# The keys in features in labels represent an edge. Every edge in one dictionary should be present in another one with the appropriate label - 0/1
def writeTrain(np_train, np_output, outfile, train_name="train", label_name="labels"):
	np_dict = {train_name:np_train, label_name: np.transpose(np_output)}
	io.savemat(outfile, np_dict)

def matwrapTrain(features, labels):
	train = []
	output = []

	for edge, val in features.iteritems():
		train.append(val)
		output.append(labels[edge])

	np_train = np.array(train)
	np_output = np.array(output)
	return (np_train, np_output)

def writeSparseMat(Ai, Aj, Av, l1, l2, l3, fname):
	np_Ai= np.array(Ai)
	np_Aj= np.array(Aj)
	np_Av= np.array(Av)
	np_dict= {l1:np_Ai, l2:np_Aj, l3:np_Av}	
	io.savemat(fname, np_dict)
