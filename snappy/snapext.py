import snap
import dateutil.parser 
from datetime import *

class EdgeInfo:
	def __init__(self, created_at, weight):
		self.created_at = dateutil.parser.parse(created_at).replace(tzinfo=None)
		self.weight = weight

class EUNGraph():
	def __init__(self):
		self.G = snap.TUNGraph.New()	
		self.edge_info = {}

	def AddNode(self, u):
		return self.G.AddNode(u)

	def AddEdge(self, u, v, created_at, weight):
		info = EdgeInfo(created_at, weight)
		tup = (u,v)
		self.edge_info[tup] = info
		return self.G.AddEdge(u,v)

	def GetNI(self, u):
		return self.G.GetNI(u)


	def IsNode(self, u):
		return self.G.IsNode(u)

	def IsEdge(self, u, v):
		return self.G.IsEdge(u, v)

	def GetNodes(self):
		return self.G.GetNodes()

	def Nodes(self):
		return self.G.Nodes()

	def GetEdges(self):
		return self.G.GetEdges()

	def Edges(self):
		return self.G.Edges()

	def GetEdgeInfo(self, u, v):
		tup = (u,v)
		return self.edge_info[tup]

	def GetWeight(self, u, v):
		tup = (u,v)

		if tup in self.edge_info:
			return self.edge_info[tup].weight

		return -1

	def GetRndNId(self):
		return self.G.GetRndNId()

	def created_at(self, u, v):
		tup = (u,v)

		if tup in self.edge_info:
			return self.edge_info[tup].created_at
		
		return datetime.max
