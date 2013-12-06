from db.interface import * 
from analysis.graphutils import *
import sys

# @author - Vikesh Khanna
# Builds a base graph till date1, then creates a delta graph from date1 to date2. 
# Calculates the number of hops between a pair of nodes in the base graph that formed an edge in the delta graph

# Date format MUST be YYYY-MM-DD HH:mm:ss

def hops(Gcollab_base, Gcollab_delta):
	hop_cache = {}

	for edge in Gcollab_delta.Edges():
		u = edge.GetSrcNId()
		v = edge.GetDstNId()

		# u = v because of the union repo owners in query. Ignore that case.
		if u!=v and Gcollab_base.IsNode(u) and Gcollab_base.IsNode(v) and not Gcollab_base.IsEdge(u,v):
			num_hops = snap.GetShortPath(Gcollab_base, u, v)
		
			if num_hops not in hop_cache:
				hop_cache[num_hops] = 0

			hop_cache[num_hops]+=1

	return hop_cache

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
	

def main(args):
	db = args[0]
	date1 = args[1]
	date2 = args[2]
	action = args[3]
	supported = ["hops", "overlap"]

	if action not in supported:
		print("Unsupported action. Supported actions are: ")
		print(supported)
		sys.exit(1)

	reader = DBReader(db)
	uid = reader.uid()
	print("#uid cache. Length=%d"%len(uid))

	collab_base = reader.collaborators(None, date1)
	print("#collab_base. Length=%d"%len(collab_base))

	Gcollab_base = get_db_graph(Graph.COLLAB, uid, collab_base)
	print("#Gcollab_base Length=%d"%Gcollab_base.GetNodes())

	if action==supported[0]:
		collab_delta = reader.collaborators(date1, date2)
		Gcollab_delta = get_db_graph(Graph.COLLAB, uid, collab_delta)

		hop_cache = hops(Gcollab_base, Gcollab_delta)

		print("#hops\tnumber of closures")
		for key in sorted(hop_cache.keys()):
			print("%d\t%d"%(key, hop_cache[key]))

	elif action==supported[1]:
		pull_base = reader.pull(None, date1)
		print("pull_base ready. Length=%d"%len(pull_base))
		Gpull_base = get_db_graph(Graph.PULL, uid, pull_base)
		print("Pull Graph ready. Nodes=%d"%Gpull_base.GetNodes())

		follow_base = reader.followers(None, date1)
		print("follow_base ready. Length=%d"%len(follow_base))
		Gfollow_base = get_db_graph(Graph.FOLLOW, uid, follow_base)
		print("Pull Graph ready. Nodes=%d"%Gfollow_base.GetNodes())

		# How many people who collaborated shared a pull request	
		pull_overlap = prop_overlap(Gpull_base, Gcollab_delta)
		print("Pull overlap: %f"%pull_overlap)

		follow_overlap = prop_overlap(Gfollow_base, Gcollab_delta)
		print("Followers overlap: %f"%follow_overlap)

# base graph = till date1
# delta graph = date1 to date2
# action - hop/overlap

if __name__=="__main__":
	if len(sys.argv)<5:
		print("Usage: program.py <db> <date1> <date2> <action>")
		sys.exit(1)
	
	main(sys.argv[1:])
