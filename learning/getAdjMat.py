def getAdjMat(G):
	Ai= []
	Aj= []
	Av= []

	for e in G.Edges():
		src = e.GetSrcNId()
		dest = e.GetDstNId()

		Ai.append(src)
		Aj.append(dest)
		Av.append(1)
		Ai.append(dest)
		Aj.append(src)
		Av.append(1)

	return (Ai, Aj, Av)
