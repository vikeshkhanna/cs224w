from db.interface import * 
from analysis.graphutils import *

reader = DBReader('db/github.2012_4_12.2012_8_14.db')
collab = reader.collaborators('2012-04-12','2012-08-12')
uid = reader.uid()

G = get_db_graph(Graph.COLLAB, uid, collab)
print G.GetNodes()

follow = reader.followers('2012-04-12','2012-08-12')
G2 = get_db_graph(Graph.COLLAB, uid, follow)
print G2.GetNodes()

pull = reader.pull('2012-04-12', '2012-08-12')
G3 = get_db_graph(Graph.COLLAB, uid, pull)
print G3.GetNodes()

watch = reader.watch('2012-04-12', '2012-08-12')
G4 = get_db_graph(Graph.COLLAB, uid, watch)
print G4.GetNodes()
