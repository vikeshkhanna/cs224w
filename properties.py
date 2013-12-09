import analysis.snap
import sys
import os
from analysis.utils import *
from analysis import graphutils
from db.interface import *

def main(args):
	if len(args)<1:
		print("Usage: ./program <db> <date1> <date2>")
		sys.exit(1)

	db = args[0]
	date1 = args[1]
	date2 = args[2]
	
	reader = DBReader(db)
	uid = reader.uid()
	print("#uid cache. Length=%d"%len(uid))

	collab_base = reader.collaborators(None, date1)
	print("#collab_base. Length=%d"%len(collab_base))

	Gcollab_base = graphutils.get_db_graph(graphutils.Graph.COLLAB, uid, collab_base)
	print("#Gcollab_base. Number of nodes=%d"%Gcollab_base.GetNodes())

	G = Gcollab_base.G

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
