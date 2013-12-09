import snappy.snap as snap
from getFeatures import *
from getKHopN import *
from analysis import graphutils

# get feature graphs
# read followgraph
# first construct features dict consisting of every pair which is k hops away

def consolidate_features(base_graphs, Gcollab_delta, k):
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
		features = getFeatures(Gcollab, Gcollab_delta, graph, features)

	return features

def consolidate_features_add(base_graphs, k, Gcollab_delta):
	# Get all the k-hop features
	features = consolidate_features(base_graphs, Gcollab_delta, k)
	Gcollab_base = base_graphs[graphutils.Graph.COLLAB]
	feature_graphs = graphutils.split_feat_graphs(base_graphs)
	org = len(features)
	cnt = 0

	# Add positive features for edges that are not k-hop
	for edge in Gcollab_delta.Edges():
		if cnt<org:
			u = edge.GetSrcNId()
			v = edge.GetDstNId()
			tup = (u,v)

			# Not k-hop and not an edge in base graph
			if (u,v) not in features and (v,u) not in features and not Gcollab_base.IsEdge(u,v):
				features[tup] = get_all_features(feature_graphs, u, v)
				cnt+=1
		else:
			break

	print("Added %d"%(cnt-org))
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

def consolidate_labels_add(features, Gcollab_base, Gcollab_delta):
	# Get the labels
	labels = consolidate_labels(features, Gcolab_delta)
	total_count = len(labels)
	total_positive = sum([val for key,val in labels.iteritems() if val==1])


