import path
import snappy.snap as snap
import learning.interface as interface
import learning.getAdjMat as getAdjMat
G= snap.GenRndGnm(snap.PUNGraph, 20, 100)
PR= snap.TIntFltH()
snap.GetPageRank(G, PR)
for item in PR:
	print item.GetKey(), item.GetDat()
# Write adjacency matrix of G in a .mat file
Ai, Aj= getAdjMat.getAdjMat(G)
Av= list()
normalizer= [0] * 20
for i in range(0, len(Ai)):
	normalizer[Ai[i]]= normalizer[Ai[i]] + 1
for i in range(0, len(Ai)):
	Av[i]= 1/ normalizer[Ai[i]]
interface.writeSparseMat(Ai, Aj, Av, 'Ai', 'Aj', 'Av', 'test_adj.mat')



