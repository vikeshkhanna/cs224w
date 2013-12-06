import snappy.snap as snap
from consolidateFeatures import *
import scipy.io as io
import numpy as np

# The keys in features in labels represent an edge. Every edge in one dictionary should be present in another one with the appropriate label - 0/1
def write(features, labels, outfile, train_name="train", label_name="labels"):
	train = []
	output = []

	for edge, val in features.iteritems():
		train.append(val)
		output.append(labels[edge])

	np_train = np.array(train)
	np_output = np.array(output)
	np_dict = {train_name:np_train, label_name:np_output}
	io.savemat(outfile, np_dict)

