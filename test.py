import sys, os
from db.interface import *
from learning import interface
from analysis import graphutils
from learning import consolidateFeatures
from mlabwrap import mlab
import numpy as np
from learning import getAdjMat
from learning import testForSource
from walk import runrw
from walk import evaluate
from utils.logger import *
from utils.helper import *
import random
 
LEARNING_ROOT="learning/"
FEATURES="testfeatures"
LABELS="ytest"

def main(args):
	db = args[0]
	date1 = args[1]
	date2 = args[2]
	date3 = args[3]
	k = int(args[4])
	OUTFILE=args[5]

	if len(args)>=7:
		beta = float(args[6])
		bstart = beta
		bfinish = beta
	else:
		bstart = 0
		bfinish = 20

	reader = DBReader(db)
	print("Getting uid")
	uid = reader.uid()

	print("Getting all the base graphs")
	feature_graphs = graphutils.get_feat_graphs(db, uid, None, date1)
	Gcollab_base = graphutils.get_collab_graph(db, uid, date3, date1)
	base_graphs = graphutils.get_base_dict(Gcollab_base, feature_graphs)

	print("Getting Gcollab_delta graph")
	Gcollab_delta = graphutils.get_collab_graph(db, uid, date1, date2)

	# from base graph take a random source node in every iteration
	baseG = base_graphs[graphutils.Graph.COLLAB]
	featG = graphutils.split_feat_graphs(base_graphs)

	deltaNIDs = [node.GetId() for node in Gcollab_delta.Nodes()]
	baseNIDs = [node.GetId() for node in baseG.Nodes()]
	common_nodes = list(set(deltaNIDs).intersection(baseNIDs))
	
	ktop = 20
	subGraphK= 10 
	f = open(OUTFILE,"w")

	print_and_log("# Beta\tRecall\tAvg. Rank\tPrec 20\n", f)		
	n_iterations = 10
	it = 0
	sources = []

	while it < n_iterations:
		src  = random.choice(common_nodes)
		subBaseG= graphutils.getSubGraph(baseG, src, subGraphK)
		#print 'subgraph: ', subBaseG.GetNodes(), subBaseG.GetEdges()
		actual = evaluate.getYList(subBaseG, Gcollab_delta, src)
		#actual = evaluate.getYList(baseG, Gcollab_delta, src)
	
		# Consider source node if it forms at least one edge in delta graph
		if len(actual)>0:
			sources.append(src)
			common_nodes.remove(src)
			it += 1
		else:
			print("Warning. Ignoring node with 0 new edges")
	print 'number of nodes and edges in graph:', baseG.GetNodes(), baseG.GetEdges()

	for beta in frange(bstart, bfinish, 4):
		total_recall = 0
		total_avg_rank= 0
		total_preck = 0

		for src in sources:
			subBaseG= graphutils.getSubGraph(baseG, src, subGraphK)
			print 'sub graph nodes:', subBaseG.GetNodes()
			print 'sub graph edges:', subBaseG.GetEdges()
			topIDs = runrw.runrw(subBaseG, featG, src, beta)	
			#topIDs = runrw.runrw(baseG, featG, Gcollab_delta, src, beta)	

			# compare topIDs with list of labels already formed	
			actual = evaluate.getYList(subBaseG, Gcollab_delta, src)
			#actual = evaluate.getYList(baseG, Gcollab_delta, src)
	
			# ignore if the node did not form an edge in the delta	
			recall, preck, average_rank = evaluate.getAccuracy(topIDs, actual, ktop)	
			print recall, preck, average_rank
				
			total_recall+=recall
			total_avg_rank += average_rank
			total_preck += len(preck)
			
		num = float(n_iterations)
		print_and_log("%f\t%f\t%f\t%f\n"%(beta, total_recall/num, total_avg_rank/num, total_preck/num), f)
	
	f.close()	
		
# base graph = till date1
# delta graph = date1 to date2
# This file calls consolidate_features for the base graph, consolidate_labels for the delta graph and writes the .mat file
# based on the basename. It also needs the k (number of hops) parameter
if __name__=="__main__":
	if len(sys.argv)<6:
		print("Usage: program.py <db> <date1> <date2> <date3> <k hops> <outfile> [beta: optional - iterates if not given]")
		print("# Base Graph - date3 to date1. Delta graph - date1 to date2. Feature graph - beginning of time to date1")
		sys.exit(1)
	
	main(sys.argv[1:])
