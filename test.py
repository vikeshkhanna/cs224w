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
OUTFILE="test.out"

def main(args):
	db = args[0]
	date1 = args[1]
	date2 = args[2]
	k = int(args[3])

	if len(args)>=5:
		beta = args[4]
		bstart = beta
		bfinish = beta
	else:
		bstart = 0
		bfinish = 4

	reader = DBReader(db)
	print("Getting uid")
	uid = reader.uid()

	print("Getting all the base graphs")
	base_graphs = graphutils.get_db_graphs(db, uid, None, date1)

	print("Getting Gcollab_delta graph")
	Gcollab_delta = graphutils.get_collab_graph(db, uid, date1, date2)

	n_iterations = 25

	# from base graph take a random source node in every iteration
	baseG = base_graphs[graphutils.Graph.COLLAB]
	featG = graphutils.split_feat_graphs(base_graphs)

	deltaNIDs = [node.GetId() for node in Gcollab_delta.Nodes()]
	baseNIDs = [node.GetId() for node in baseG.Nodes()]
	common_nodes = list(set(deltaNIDs).intersection(baseNIDs))
	
	ktop = 20
	f = open(OUTFILE,"w")

	print_and_log("# Beta\tRecall\tAvg. Rank\tPrec 20\n", f)		

	n_iterations = 10
	it = 0
	sources = []

	while it < n_iterations:
		src  = random.choice(common_nodes)
		actual = evaluate.getYList(baseG, Gcollab_delta, src)
	
		# Consider source node if it forms at least one edge in delta graph
		if len(actual)>0:
			sources.append(src)
			common_nodes.remove(src)
			it += 1
		else:
			print("Warning. Ignoring node with 0 new edges")

	for beta in frange(bstart, bfinish, 0.25):
		total_recall = 0
		total_avg_rank= 0
		total_preck = 0

		for src in sources:
			topIDs = runrw.runrw(baseG, featG, Gcollab_delta, src, beta)	

			# compare topIDs with list of labels already formed	
			actual = evaluate.getYList(baseG, Gcollab_delta, src)
	
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
	if len(sys.argv)<5:
		print("Usage: program.py <db> <date1> <date2> <k hops> [beta: optional - iterates if not given]")
		sys.exit(1)
	
	main(sys.argv[1:])
