from db.interface import * 
from analysis.graphutils import *
import snap
reader = DBReader('db/github.2012_4_12.2012_8_14.db')
collab = reader.collaborators('2012-04-12','2012-08-12')
uid = reader.uid()

G = get_db_graph(Graph.COLLAB, uid, collab)
snap.SaveEdgeList(G, 'collab.txt')
print G.GetNodes()

follow = reader.followers('2012-04-12','2012-08-12')
G2 = get_db_graph(Graph.COLLAB, uid, follow)
snap.SaveEdgeList(G2, 'follow.txt')
print G2.GetNodes()

pull = reader.pull('2012-04-12', '2012-08-12')
G3 = get_db_graph(Graph.COLLAB, uid, pull)
snap.SaveEdgeList(G3, 'pull.txt')
print G3.GetNodes()

watch = reader.watch('2012-04-12', '2012-08-12')
G4 = get_db_graph(Graph.COLLAB, uid, watch)
snap.SaveEdgeList(G, 'watch.txt')
print G4.GetNodes()
