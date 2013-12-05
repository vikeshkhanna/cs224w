import snap

class Graph:
	COLLAB = 1
	PULL = 2 
	FOLLOW = 3
	WATCH = 4
	FORK = 5

def construct(edgelist):
	G = snap.TUNGraph.New()

	for edge in edgelist:
		u = edge[0]
		v = edge[1]

		if not G.IsNode(u):
			G.AddNode(u)
	
		if not G.IsNode(v):
			G.AddNode(v)

		if not G.IsEdge(u,v):
			G.AddEdge(u, v)

	return G

def get_db_graph(graph_type, uid, dbresponse):
	edgelist = []

	for row in dbresponse:
		try:
			edgelist.append((uid[row[0]], uid[row[1]]))
		except KeyError:
			pass
			# Ignore if some user is not found in uid

	return construct(edgelist)
	
