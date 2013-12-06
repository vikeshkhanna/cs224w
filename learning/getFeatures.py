# filters the pairs of nodes in 'pairs' and returns features from featG for pairs such that both nodes are present in featG
import snappy.snap as snap 
from getCoefficients import *

def getFeatures(baseG, featG, pairs):
	delset= set()
	# from every start node, get all the nodes which are upto k hops away.
	for u, v in pairs:
		uNode= baseG.GetNI(u)
		vNode= baseG.GetNI(v)
		# ensure that basenodeID is lower than neighborID
		if (u > v):
			u= u + v
			u= u - v
		# see if both of these nodes are in feat graph
		if not (featG.IsNode(u) and featG.IsNode(v)):
			# delete this pair from the pair dict
			delset.add((u, v))
			continue

		uFNode= featG.GetNI(u)
		vFNode= featG.GetNI(v)
		# calculate all coefficients for u, v
		pairs[(u, v)].append(featG.GetWeight(u,v))  # featG must be undirected, GetWeight=-1 for no edge.
		pairs[(u, v)].append(getCommonNeighbor(uFNode, vFNode))
		pairs[(u, v)].append(getJaccard(uFNode, vFNode))
		pairs[(u, v)].append(getAdamicAdar(uFNode, vFNode))
	
	for (u, v) in delset:
		del pairs[(u, v)]

	return pairs

