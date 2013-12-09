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
import random

 
LEARNING_ROOT="learning/"
FEATURES="testfeatures"
LABELS="ytest"
OUTFILE="test.out"

def print_and_log(s, f):
	f.write(s)
	print(s)
	

def main(args):
	db = args[0]
	date1 = args[1]
	date2 = args[2]
	k = int(args[3])

	reader = DBReader(db)
	print("Getting uid")
	uid = reader.uid()

	print("Getting Collab delta")
	collab_delta = reader.collaborators(date1, date2)
	reader.close()

	print("Getting all the base graphs")
	base_graphs = graphutils.get_db_graphs(db, uid, None, date1)

	print("Getting Gcollab_delta graph")
	Gcollab_delta = graphutils.get_db_graph(graphutils.Graph.COLLAB, uid, collab_delta) 

	n_iterations = 25

	# from base graph take a random source node in every iteration
	baseG= base_graphs[graphutils.Graph.COLLAB]
	featG= graphutils.split_feat_graphs(base_graphs)

	deltaNIDs = [node.GetId() for node in Gcollab_delta.Nodes()]
	baseNIDs = [node.GetId() for node in baseG.Nodes()]
	common_nodes = list(set(deltaNIDs).intersection(baseNIDs))
	
	ktop = 20
	f = open(OUTFILE,"w")

	for beta in range(0, 4, 0.1):
		total_recall = 0
		total_avg_rank= 0
		total_preck = 0
		n_iterations = 25

		for i in range(0, n_iterations):
			src = random.choice(common_nodes)
			common_nodes.remove(src)
			topIDs = runrw.runrw(baseG, featG, Gcollab_delta, src, beta)	

			# compare topIDs with list of labels already formed	
			actual = evaluate.getYList(baseG, Gcollab_delta, src)
			recall, preck, average_rank = evaluate.getAccuracy(topIDs, actual, ktop)	

			total_recall+=recall
			total_avg_rank += average_rank
			total_preck += len(preck)
			
		num = float(n_iterations)
		print_and_log("# Beta\tRecall\tAvg. Rank\tPrec 20\n", f)		
		print_and_log("%f\t%f\t%f\t%f\n"%(beta, total_recall/num, total_avg_rank/num, total_preck/num), f)
	
	f.close()	
		
# base graph = till date1
# delta graph = date1 to date2
# This file calls consolidate_features for the base graph, consolidate_labels for the delta graph and writes the .mat file
# based on the basename. It also needs the k (number of hops) parameter
if __name__=="__main__":
	if len(sys.argv)<5:
		print("Usage: program.py <db> <date1> <date2> <k hops>")
		sys.exit(1)
	
	main(sys.argv[1:])
