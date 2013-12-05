import snap

def getKHopN(G, node, k):
	s= set()
	for i in range(1, k+1):
		v= snap.TIntV()
		snap.GetNodesAtHop(G, node, i, v, False)
		# add node IDs in v to s
		for item in v:
			s.add(item)
	return s

		
	
