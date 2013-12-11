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
import snappy.snap as snap
import snappy.snapext as snapext
 
LEARNING_ROOT="learning/"
FEATURES="testfeatures"
LABELS="ytest"

def main(args):
	db = args[0]
	date1 = args[1]
	userid = args[2]
	
	k=2
	beta= 0

	reader = DBReader(db)
	print("Getting uid")
	uid = reader.uid()
	src = uid[userid]

	print("Userid, rowid: %s, %d"%(userid, src))

	print("Getting all the base graphs")

	
	'''
	Gcollab_base = graphutils.get_collab_graph(db, uid)
	assert(Gcollab_base.IsNode(src))

	feature_graphs = graphutils.get_feat_graphs(db, uid, None, date1)
	base_graphs = graphutils.get_base_dict(Gcollab_base, feature_graphs)

	# from base graph take a random source node in every iteration
	baseG = base_graphs[graphutils.Graph.COLLAB]
	featG = graphutils.split_feat_graphs(base_graphs)

	'''
	followers = reader.followers()
	baseG = graphutils.get_db_graph(graphutils.Graph.FOLLOW, uid, followers)
	Gp = snapext.EUNGraph()
	featG = [Gp, Gp, Gp]
	
	subBaseG= graphutils.getSubGraph(baseG, src, 5)
	topIDs = runrw.runrw(subBaseG, featG, src, beta)[:20]	
	print reader.get_users(topIDs)
		
# base graph = till date1
# delta graph = date1 to date2
# This file calls consolidate_features for the base graph, consolidate_labels for the delta graph and writes the .mat file
# based on the basename. It also needs the k (number of hops) parameter
if __name__=="__main__":
	if len(sys.argv)<4:
		print("Usage: program.py <db> <date1> <userid>")
		sys.exit(1)
	
	main(sys.argv[1:])
