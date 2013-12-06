import snappy.snap as snap
from getFeatures import *
from getKHopN import *

# get feature graphs
# read followgraph
# first construct features dict consisting of every pair which is k hops away

def consolidate_features(Gcollab, Gfollow, Gpull, Gwatch, Gfork):
	k= 2	# 2 hops away
	features = {}

	for node in Gcollab.Nodes():
		nodeID= node.GetId()
		for neighborID in getKHopN(Gcollab.G, nodeID, k):
			neighbor= Gcollab.GetNI(neighborID)
			if(neighborID > nodeID):	# swap
				nodeID= neighborID + nodeID
				neighborID= nodeID - neighborID
				nodeID= nodeID - neighborID
			if (nodeID, neighborID) in features:
				continue
			features[(nodeID, neighborID)]= []
				
	features = getFeatures(Gcollab, Gfollow, features)
	features = getFeatures(Gcollab, Gpull, features)
	features = getFeatures(Gcollab, Gwatch, features)
	features = getFeatures(Gcollab, Gfork, features)

	return features

def consolidate_labels(features, Gcollab_delta):
	labels = {}

	for edge, feat in features.iteritems():
		u = edge[0]
		v = edge[1]

		if(Gcollab_delta.IsEdge(u,v)):
			labels[edge] = 1
		else:
			labels[edge] = 0

	return labels	
