# filters the pairs of nodes in 'pairs' and returns features from featG for pairs such that both nodes are present in featG
import snappy.snap as snap 
from getCoefficients import *

# Gets the features for the given pair of nodes. Also deletes the nodes that are not present in feature graph
def getFeatures(baseG, featG, pairs):
	delset= set()

	# from every start node, get all the nodes which are upto k hops away.
	for u, v in pairs:
		uNode= baseG.GetNI(u)
		vNode= baseG.GetNI(v)
		# ensure that basenodeID is lower than neighborID
		if (u > v):
			temp = u
			u = v
			v= temp			
		# see if both of these nodes are in feat graph
		if not (featG.IsNode(u) and featG.IsNode(v)):
			# delete this pair from the pair dict
			delset.add((u, v))
			continue

		uFNode= featG.GetNI(u)
		vFNode= featG.GetNI(v)
		tup = (u,v)

		features = get_features(featG, u, v)
		
		for feature in features:
			pairs[tup].append(feature)

	for (u, v) in delset:
		del pairs[(u, v)]

	return pairs

# Gets the features given two node IDs
def get_features(featG, u, v):
	features = []

	# If either node does not exist in the feature graph
	# Not the first -1 is because GetWeight returns -1 for no edge
	if not featG.IsNode(u) or not featG.IsNode(v):
		return [featG.GetWeight(u,v),0,0,0]

	uFNode = featG.GetNI(u)
	vFNode = featG.GetNI(v)

	# calculate all coefficients for u, v
	features.append(featG.GetWeight(u,v))  # featG must be undirected, GetWeight=-1 for no edge.
	features.append(len(getCommonNeighbor(uFNode, vFNode)))
	features.append(getJaccard(uFNode, vFNode))
	features.append(getAdamicAdar(featG, uFNode, vFNode))

	return features

# Get all the features for 2 nodes
def get_all_features(feature_graphs, u, v):
	features = []

	for graph_type, graph in feature_graphs.iteritems():
		feat = get_features(graph, u, v)
			
		for val in feat:
			features.append(val)	

	return features

# Get a dictionary for (s,v):[features] where s is the start node and v are all other nodes - features
def get_walk_features(Gcollab, feature_graphs, start):
	features = {}

	for vnode in Gcollab.Nodes():
		v = vnode.GetId()

		if start!=v:
			tup = (start, v)
			features[tup] = get_all_features(feature_graphs, start, v)
			
	return features
