import snap
import os
import math
import snap
import sys

def mle(hist):
	freq = [item[1] for item in hist]
	n = sum(freq)

	alpha = 1 + n*(1.0/sum([item[1]*math.log(item[0]) for item in hist]))
	return alpha

def get_graph(path):
	path = os.path.abspath(path)
	return snap.LoadEdgeList(snap.PUNGraph, path)

def get_degree_histogram(G):
	vec = snap.TIntPrV()
	snap.GetDegCnt(G, vec)
	hist = []

	for pair in vec:
		hist.append((pair.GetVal1(), pair.GetVal2()))

	return hist

def get_wcc_histogram(G):
	vec = snap.TIntPrV()
	snap.GetWccSzCnt(G, vec)
	
	hist = []

	for pair in vec:
		hist.append((pair.GetVal1(), pair.GetVal2()))

	return	hist 

