from mlabwrap import mlab
import numpy as np
from learning import getFeatures
from learning import interface

def testForSource(Ai, Aj, Av, Gcollab_base, feature_graphs, src, beta):
	# Get the features from G for the given source node
	features = getFeatures.get_walk_features(Gcollab_base, feature_graphs, src)
	newAi= Ai
	newAj= Aj
	# convert nodeorder into a dict for mapping
	# mapping[oldID]= newID
	# nodeorder[newID-1]= oldID
	# newID starts from 1, and not 0

	mapping = {}
	rmap = {}
	
	cnt = 1
	flat_features = []

	for tup, feature in features.iteritems():
		v = tup[1]
		mapping[v] = cnt
		rmap[cnt] = v

		flat_features.append(feature)
		cnt+=1
	
	for i in range(len(Ai)):
		newAi[i]= mapping[Ai[i]]
		newAj[i]= mapping[Aj[i]]
	
	newSrcID = mapping[src]

	np_Ai, np_Aj, np_Av = interface.sparsePyToMat(Ai, Aj, Av)

	np_F = np.array(flat_features)
	mlab.path(mlab.path(), "learning/")

	#print np_Ai, np_Aj, np_Av, np_F, newSrcID, beta, basename

	np_newIDs= mlab.runRW(np_Ai, np_Aj, np_Av, np_F, newSrcID, beta)
	newIDs= np_newIDs.tolist()

	# convert newIDs to original IDs
	origIDs= []

	for new_id in newIDs:
		origIDs.append(rmap[new_id[0]])

	return origIDs
