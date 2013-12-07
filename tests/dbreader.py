import path
from db.interface import * 
from analysis.graphutils import *

reader = DBReader('../db/github.2012_4_12.2012_8_14.db')
#reader = DBReader('../db/github.2012_4_12.2012_8_14.db')

collab = reader.collaborators()
uid = reader.uid()

G = get_db_graph(Graph.COLLAB, uid, collab)
print G.GetNodes()

u = G.G.GetRndNId()
v = G.G.GetRndNId()
print(G.GetWeight(u,v))

follow = reader.followers()
G2 = get_db_graph(Graph.COLLAB, uid, follow)
print G2.GetNodes()

pull = reader.pull()
G3 = get_db_graph(Graph.COLLAB, uid, pull)
print G3.GetNodes()

watch = reader.watch()
G4 = get_db_graph(Graph.COLLAB, uid, watch)
print G4.GetNodes()
