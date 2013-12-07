def getAdjMat(G):
	Ai= list();
	Aj= list();
	for e in G.Edges():
		Ai.append(e.GetSrcNId())
		Aj.append(e.GetDstNId())
		Ai.append(e.GetDstNId())
		Aj.append(e.GetSrcNId())
	for i in range(0, len(Ai)):
		Ai[i]= Ai[i]+1
		Aj[i]= Aj[i]+1
	return (Ai, Aj)
