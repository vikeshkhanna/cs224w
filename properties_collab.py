from db.interface import * 
import snappy.snap as snap
import random
from analysis.graphutils import *
import sys

# @author - Vikesh Khanna
# Builds a base graph till date1, then creates a delta graph from date1 to date2. 
# Calculates the number of hops between a pair of nodes in the base graph that formed an edge in the delta graph

# Date format MUST be YYYY-MM-DD HH:mm:ss

def hops(Gcollab_base, Gcollab_delta):
	hop_cache = {}
	edges = [(edge.GetSrcNId(),edge.GetDstNId()) for edge in Gcollab_delta.Edges()]
	max_samples = 1000
	it = 0

	while it<max_samples:
		u,v = random.choice(edges)
		
		# u = v because of the union repo owners in query. Ignore that case.
		if u!=v and Gcollab_base.IsNode(u) and Gcollab_base.IsNode(v) and not Gcollab_base.IsEdge(u,v):
			it+=1
			print("Starting search for %d,%d"%(u,v))

			num_hops = snap.GetShortPath(Gcollab_base.G, u, v)
	
			if num_hops not in hop_cache:
				hop_cache[num_hops] = 0

			hop_cache[num_hops]+=1

	return hop_cache

def prop_hop(Gcollab_base, Gprop_base, node, k):
	total = 0	
	cnt = 0

	for v in Gcollab_base.GetNI(node).GetOutEdges():
		if Gprop_base.IsNode(v) and Gprop_base.IsNode(node):
			length = snap.GetShortPath(Gprop_base.G, node, v)
			total += length
			cnt += 1

	if cnt>0:
		return float(total)/cnt
	else:
		return -1

def prop_overlap(Gprop_base, Gcollab_delta):
	total_edges = Gcollab_delta.GetEdges()
	total_prop_overlap = 0

	for edge in Gcollab_delta.Edges():
		u = edge.GetSrcNId()
		v = edge.GetDstNId()

		# u = v because of the union repo owners in query. Ignore that case.
		if u!=v and Gprop_base.IsNode(u) and Gprop_base.IsNode(v) and Gprop_base.IsEdge(u,v):
			total_prop_overlap += 1

	return total_prop_overlap/float(total_edges)
	
def wcc(G):	
	components = snap.TIntPrV()
	snap.GetWccSzCnt(G.G, components)
	# Size, Number of Wccs of this size
	return [(comp.GetVal1(), comp.GetVal2()) for comp in components]

def main(args):
	db = args[0]
	date1 = args[1]
	date2 = args[2]
	action = args[3]
	supported = ["hops", "overlap", "prop_hop", "wcc"]

	if action not in supported:
		print("Unsupported action. Supported actions are: ")
		print(supported)
		sys.exit(1)

	reader = DBReader(db)
	uid = reader.uid()
	print("#uid cache. Length=%d"%len(uid))

	if action==supported[0]:
		Gcollab_base = get_collab_graph(db, uid, None, date1)
		Gcollab_delta = get_collab_graph(db, uid, date1, date2)

		print("#hops\tnumber of closures")
		hop_cache = hops(Gcollab_base, Gcollab_delta)

		for key in sorted(hop_cache.keys()):
			print("%d\t%d"%(key, hop_cache[key]))

	elif action==supported[1]:
		Gcollab_base = get_collab_graph(db, uid, None, date1)
		Gcollab_delta = get_collab_graph(db, uid, date1, date2)
		feature_graphs = get_feat_graphs(db, uid, None, date1)

		base_graphs = get_base_dict(Gcollab_base, feature_graphs)
		rmap = get_reverse_graph_map(base_graphs)

		for graph in feature_graphs:
			overlap = prop_overlap(graph, Gcollab_delta)
			print("%s overlap: %f"%(rmap[graph], overlap))

	elif action==supported[2]:
		Gcollab_base = get_collab_graph(db, uid, None, date1)
		print("# NodeID\tGfollow\tGfork\tGwatch")
		nodes = [node.GetId() for node in Gcollab_base.Nodes()]
		num_samples = 20
		i = 0

		feature_graphs = get_feat_graphs(db, uid, None, date1)
		base_graphs = get_base_dict(Gcollab_base, feature_graphs)
		rmap = get_reverse_graph_map(base_graphs)

		while i<num_samples:	
			u = random.choice(nodes)
			values = []

			for graph in feature_graphs:
				values.append(prop_hop(Gcollab_base, graph, u, 2))
			i+=1
	
			print("%d\t%f\t%f\t%f"%(u, values[0], values[1], values[2]))			

	elif action==supported[3]:
		Gcollab_base = get_only_collab_graph(db, uid, None, date1)
		print("Nodes=%d"%(Gcollab_base.GetNodes()))

		print("# WCC Size\tNumber of WCCs")
		rows = wcc(Gcollab_base)	

		for tup in rows:
			print("%d\t%d"%(tup[0], tup[1]))

# base graph = till date1
# delta graph = date1 to date2
# action - hop/overlap

if __name__=="__main__":
	if len(sys.argv)<5:
		print("Usage: program.py <db> <date1> <date2> <action>")
		sys.exit(1)
	
	main(sys.argv[1:])
