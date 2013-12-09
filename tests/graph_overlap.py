import path
from analysis import graphutils
from db.interface import *
import snappy.snap as snap
import utils

Gbase = utils.get_small_collab(None, utils.small_date1())
Gdelta = utils.get_small_collab(utils.small_date1(), utils.small_date2())
print("Gdelta edges: %d" % Gdelta.GetEdges())
print("Gbase edges: %d" % Gbase.GetEdges())

overlap = 0
cnt = 0

for edge in Gdelta.Edges():
	u = edge.GetSrcNId()
	v = edge.GetDstNId()

	if Gbase.IsEdge(u,v):
		overlap+=1

	cnt += 1

print("Overlap: %f"%(overlap/float(cnt)))
	


	
