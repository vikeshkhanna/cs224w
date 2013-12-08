import snappy.snap as snap
from getFeatures import *
from getKHopN import *
from analysis import graphutils

# get feature graphs
# read followgraph
# first construct features dict consisting of every pair which is k hops away

def consolidate_features(base_graphs, k):
	features = {}

	Gcollab = base_graphs[graphutils.Graph.COLLAB]
	feature_graphs = graphutils.split_feat_graphs(base_graphs)

	for node in Gcollab.Nodes():
		nodeID= node.GetId()

		for neighborID in getKHopN(Gcollab.G, nodeID, k):
			if(nodeID > neighborID):	# swap
				nodeID= neighborID + nodeID
				neighborID= nodeID - neighborID
				nodeID= nodeID - neighborID

			if (nodeID, neighborID) in features:
				continue
			features[(nodeID, neighborID)]= []
				
	for graph in feature_graphs:
		features = getFeatures(Gcollab, graph, features)

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
