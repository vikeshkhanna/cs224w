import snap

def getCommonNeighbor(u, v):
	# find number of common neighbors of n1 and n2
	return	len(set(list(u.GetOutEdges())).intersection(list(v.GetOutEdges())))



def getJaccard(u, v):
	score_in= getCommonNeighbor(u, v)
	union_neighbors= set(u.GetOutEdges()).union(v.GetOutEdges())
	if(len(union_neighbors)!=0):
		return 0
	return float(len(intersection_neighbors))/len(union_neighbors)
	


def getAdamicAdar(u, v):
	# adamic- adar score
	logsum= 0
	intersection_neighbors= set(list(u.GetOutEdges())).intersection(list(v.GetOutEdges()))

	if(len(intersection_neighbors)!=0):
		return 0
	for neighbor in intersection_neighbors:
		logoutdeg= math.log(G_base.GetNI(neighbor).GetOutDeg())
		if(logoutdeg!=0):
			logsum+= 1/logoutdeg
	return logsum

