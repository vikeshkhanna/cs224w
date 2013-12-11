from learning import consolidateFeatures
from mlabwrap import mlab
from learning import getAdjMat
from learning import testForSource
import random

def runrw(baseG, featG, src, beta):
	# get the adjacency matrix
	Ai, Aj, Av = getAdjMat.getAdjMat(baseG)
	topIDs= testForSource.testForSource(Ai, Aj, Av, baseG, featG, src, beta)
	return topIDs	

