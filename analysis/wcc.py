import snap
import sys
import os
from utils import *

def main(args):
	if len(args)<1:
		print("Usage: ./program edge_list")
		sys.exit(1)
	
	G = get_graph(args[0])
	hist = get_wcc_histogram(G)
	n = sum([item[1] for item in hist])

	print("# WCC Histogram : ")

	for pair in hist:
		print("%d\t%f"%(pair[0], float(pair[1])/n))


if __name__=="__main__":
	main(sys.argv[1:])
