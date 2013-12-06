import snappy.snap as snap
import snappy.snapext as snapext
from db.interface import *
import sys

class Graph:
	COLLAB = 'Gcollab'
	PULL = 'Gpull'
	FOLLOW = 'Gfollow'
	WATCH = 'Gwatch'
	FORK = 'Gfork'

def construct(edgelist):
	G = snapext.EUNGraph()

	for edge in edgelist:
		u = edge[0]
		v = edge[1]
		created_at = edge[2]
		weight= edge[3] + 1

		if not G.IsNode(u):
			G.AddNode(u)
	
		if not G.IsNode(v):
			G.AddNode(v)

		if not G.IsEdge(u, v):
			G.AddEdge(u, v, created_at, weight)

	return G

def get_db_graph(graph_type, uid, dbresponse):
	edgelist = []

	for row in dbresponse:
		try:
			edgelist.append((uid[row[0]], uid[row[1]], row[2], row[3]))
		except KeyError:
			#sys.stderr.write("Skipping %s, %s as one of them was not in uid\n"%(row[0], row[1]))
			pass
			# Ignore if some user is not found in uid

	return construct(edgelist)

def get_db_graphs(db, uid, min_date=None, max_date=None):
	reader = DBReader(db)

	collab = reader.collaborators(min_date, max_date)
	Gcollab = get_db_graph(Graph.COLLAB, uid, collab)
	
	follow = reader.followers(min_date, max_date)
	Gfollow = get_db_graph(Graph.FOLLOW, uid, follow)

	pull = reader.pull(min_date, max_date)
	Gpull = get_db_graph(Graph.PULL, uid, pull)

	watch = reader.watch(min_date, max_date)
	Gwatch = get_db_graph(Graph.WATCH, uid, watch)

	fork = reader.watch(min_date, max_date)
	Gfork = get_db_graph(Graph.FORK, uid, fork)

	reader.close()
	return {Graph.COLLAB: Gcollab, Graph.FOLLOW:Gfollow, Graph.PULL: Gpull, Graph.WATCH: Gwatch, Graph.FORK: Gfork}
