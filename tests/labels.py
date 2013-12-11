import path
from db.interface import *
from analysis.graphutils import *
from learning.consolidateFeatures import *
from utils import *

db = get_small_db()
reader = DBReader(db)
uid = reader.uid()

Gcollab_base = get_collab_graph(db, uid, None, small_date1())
Gcollab_delta = get_collab_graph(db, uid, small_date1(), small_date2())

cnt_yes = 0
cnt_no = 0
cnt_total = 0

for node in Gcollab_base.Nodes():
	u = node.GetId()
	khops = getKHopN(Gcollab_base, u, 2)

	for v in khops:
		assert not Gcollab_base.IsEdge(u, v)

		if Gcollab_delta.IsEdge(u,v):
			cnt_yes+=1
		else:
			cnt_no+=1

		cnt_total +=1

l = float(cnt_total)

print("Positive samples=%d, %f"%(cnt_yes, cnt_yes/float(l)))
print("Negative samples=%d, %f"%(cnt_no, cnt_no/float(l)))
