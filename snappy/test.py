import snapext
from datetime import *

G = snapext.EUNGraph()
G.AddNode(1)
G.AddNode(2)
G.AddNode(3)

G.AddEdge(1, 2, datetime.now(), 1)
G.AddEdge(1,3)
G.AddEdge(2,3, weight=5)

