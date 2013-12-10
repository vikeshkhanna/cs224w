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


def getKHopN(G, node, k):
	s = set()
	for i in range(2, k+1):
		v= snap.TIntV()
		snap.GetNodesAtHop(G.G, node, i, v, False)
		# add node IDs in v to s
		for item in v:
			s.add(item)
	return s

		
	
def getSubGraph(G, source, k):
	nodes= getKHopN(G, source, k)
	# to nodes add all the neighbors of source
	nodes.add(source)
	sourceNode= G.GetNI(source)
	for neighborID in sourceNode.GetOutEdges():
		nodes.add(neighborID)
	
	# insert nodes into TIntV
	nodesV= snap.TIntV()	
	
	for node in nodes:
		nodesV.Add(node)
	subG= snap.GetSubGraph(G.G, nodesV)
	return subG

	
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

	# Pull is now a part of collab graph   
	# pull = reader.pull(min_date, max_date)
	# Gpull = get_db_graph(Graph.PULL, uid, pull)

	watch = reader.watch(min_date, max_date)
	Gwatch = get_db_graph(Graph.WATCH, uid, watch)

	fork = reader.watch(min_date, max_date)
	Gfork = get_db_graph(Graph.FORK, uid, fork)

	reader.close()
	return {Graph.COLLAB: Gcollab, Graph.FOLLOW:Gfollow, Graph.WATCH: Gwatch, Graph.FORK: Gfork}

def get_feat_graphs(db, uid, min_date=None, max_date=None):
	reader = DBReader(db)

	follow = reader.followers(min_date, max_date)
	Gfollow = get_db_graph(Graph.FOLLOW, uid, follow)

	watch = reader.watch(min_date, max_date)
	Gwatch = get_db_graph(Graph.WATCH, uid, watch)

	fork = reader.watch(min_date, max_date)
	Gfork = get_db_graph(Graph.FORK, uid, fork)

	reader.close()
	return {Graph.FOLLOW:Gfollow, Graph.WATCH: Gwatch, Graph.FORK: Gfork}

def get_base_dict(Gcollab, feature_graphs):
	base_graphs = {}

	for key,val in feature_graphs.iteritems():
		base_graphs[key] = val

	base_graphs[Graph.COLLAB] = Gcollab

	return base_graphs

def get_collab_graph(db, uid, min_date=None, max_date=None):
	reader = DBReader(db)

	collab = reader.collaborators(min_date, max_date)
	Gcollab = get_db_graph(Graph.COLLAB, uid, collab)
	
	reader.close()
	return Gcollab	

def split_feat_graphs(base_graphs):
	feature_graphs = []

	# THIS ORDER MUST BE MAINTAINED, otherwise feature vectors will keep changing order
	# Gfollow, Gfork, Gwatch
	for graph_type in sorted(base_graphs.keys()):
		graph = base_graphs[graph_type]

		if graph_type!=Graph.COLLAB:
			feature_graphs.append(graph)

	return feature_graphs

def get_reverse_graph_map(base_graphs):
	rmap = {}

	for graph_type in sorted(base_graphs.keys()):
		graph = base_graphs[graph_type]
		rmap[graph] = graph_type

	return rmap
