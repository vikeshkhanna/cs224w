import snap
from getFeatures import *
from getKHopN import *

# get feature graphs
# read followgraph
# first construct features dict consisting of every pair which is k hops away
G= snap.LoadEdgeList(snap.PUNGraph, "collab.txt", 0, 1)
k= 2	# 2 hops away
features= dict()
for node in G.Nodes():
	nodeID= node.GetId()
	for neighborID in getKHopN(G, nodeID, k):
		neighbor= G.GetNI(neighborID)
		if(neighborID > nodeID):	# swap
			nodeID= neighborID + nodeID
			neighborID= nodeID - neighborID
			nodeID= nodeID - neighborID
		if (nodeID, neighborID) in features:
			continue
		features[(nodeID, neighborID)]= list()
			
followG= snap.LoadEdgeList(snap.PUNGraph, "follow.txt", 0, 1)
features= getFeatures(G, followG, features)
del followG
pullG= snap.LoadEdgeList(snap.PUNGraph, "pull.txt", 0, 1)
features= getFeatures(G, pullG, features)
del pullG
watchG= snap.LoadEdgeList(snap.PUNGraph, "watch.txt", 0, 1)
features= getFeatures(G, watchG, features)
del watchG
print features



