import analysis.snap
import sys
import os
from analysis.utils import *
from db.interface import *

def main(args):
	if len(args)<1:
		print("Usage: ./program edge_list")
		sys.exit(1)
	
	G = get_graph(args[0])
	hist = get_degree_histogram(G)
	n = G.GetNodes()

	print("MLE estimate of alpha: %f"%mle(hist))
	
	mxWccSize = snap.GetMxWccSz(G)
	print("Fraction of nodes in the largest weakly connected component: %f"%mxWccSize)

	clustCoff = snap.GetClustCf(G)
	print("Clustering coefficient: %f"%clustCoff)

	avgDeg = sum([item[0]*item[1] for item in hist])/float(n)
	print("Average Degree: %f"%avgDeg)


	wccHist = get_wcc_histogram(G)
	print("WCC Histogram : ")
	print(wccHist)

	print(mle(wccHist))

if __name__=="__main__":
	main(sys.argv[1:])	
