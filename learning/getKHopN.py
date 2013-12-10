import snappy.snap as snap

def getKHopN(G, node, k):
	print '*****************DEPRICATED: GetKHopN***********'
	s = set()
	for i in range(2, k+1):
		v= snap.TIntV()
		snap.GetNodesAtHop(G, node, i, v, False)
		# add node IDs in v to s
		for item in v:
			s.add(item)
	return s

		
	
