from mlabwrap import mlab
import numpy as np
def testForSource(Ai, Aj, Av, feature_graphs, src):
	# Get the features from G for the given source node
	nodeorder, F= get_walk_features(G, feature_graphs, src)
	newAi= Ai
	newAj= Aj
	# convert nodeorder into a dict for mapping
	# mapping[oldID]= newID
	# nodeorder[newID-1]= oldID
	# newID starts from 1, and not 0

	mapping= dict()
	for i in range(0, len(nodeorder)):
		mapping[nodeorder[i]]= i+1
	
	for i in range(0, len(Ai)):
		newAi[i]= mapping[Ai[i]]
		newAj[i]= mapping[Aj[i]]
	
	newSrcID= mapping[src]
	np_Ai, np_Aj, np_Ak= interface.sparsePyToMat(Ai, Aj, Av)
	np_F= np.array(F)
	np_newIDs= mlab.runRW(np_Ai, np_Aj, np_Av, np_F, newSrcID, basename)
	newIDs= np_newIDs.tolist()
	# convert newIDs to original IDs
	origIDs= list()
	for id in newIDs:
		origIDs.append(nodeorder[newIDs-1])
	return origIDs
