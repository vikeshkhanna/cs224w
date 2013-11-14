import snap
import sys
import os

def main(args):
	if len(args)<1:
		print("Usage: ./program edge_list")
		sys.exit(1)

	path = os.path.abspath(args[0])
	
	vec = snap.TIntPrV()
	G = snap.LoadEdgeList(snap.PUNGraph, path)
	snap.GetDegCnt(G, vec)
	n = G.GetNodes()

	for pair in vec:
		print("%d %f"%(pair.GetVal1(), pair.GetVal2()/float(n)))

if __name__=="__main__":
	main(sys.argv[1:])
