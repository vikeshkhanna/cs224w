import snap
import sys
import os
from utils import *

def main(args):
	if len(args)<1:
		print("Usage: ./program edge_list")
		sys.exit(1)
	
	G = get_graph(args[0])
	hist = get_degree_histogram(G)
	n = G.GetNodes()

	for pair in hist:
		print("%d\t%f"%(pair[0], float(pair[1])/n))	

if __name__=="__main__":
	main(sys.argv[1:])
