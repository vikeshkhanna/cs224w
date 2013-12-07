import snappy.snap as snap
import math

def getCommonNeighbor(unode, vnode):
	# find number of common neighbors of n1 and n2
	return	set(list(unode.GetOutEdges())).intersection(list(vnode.GetOutEdges()))

def getJaccard(unode, vnode):
	score_in = getCommonNeighbor(unode, vnode)
	union_neighbors = set(list(unode.GetOutEdges())).union(list(vnode.GetOutEdges()))

	if(len(union_neighbors)==0):
		return 0

	return float(len(score_in))/len(union_neighbors)

def getAdamicAdar(G, unode, vnode):
	# adamic- adar score
	logsum = 0
	intersection_neighbors = getCommonNeighbor(unode, vnode)

	if(len(intersection_neighbors)==0):
		return 0

	for neighbor in intersection_neighbors:
		logoutdeg= math.log(G.GetNI(neighbor).GetOutDeg())

		if(logoutdeg!=0):
			logsum+= 1/logoutdeg

	return logsum

