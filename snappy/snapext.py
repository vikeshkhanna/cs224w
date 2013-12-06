import snap
from datetime import *

class EdgeInfo:
	def __init__(self, created_at=None, weight=None):
		self.created_at = created_at
		self.weight = weight

class EUNGraph():
	def __init__(self):
		self.G = snap.TUNGraph.New()	
		self.edge_info = {}

	def AddNode(self, u):
		return self.G.AddNode(u)

	def AddEdge(self, u, v, created_at=None, weight=None):
		info = EdgeInfo(created_at, weight)
		tup = (u,v)
	
		if tup not in self.edge_info:
			self.edge_info[tup] = []
		
		self.edge_info[tup].append(info)

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
			return sum([info.weight for info in self.edge_info[tup] if info.weight!=None])

		return -1
