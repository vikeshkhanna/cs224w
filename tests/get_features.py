import path
from db.interface import *
from analysis.graphutils import *
from learning.consolidateFeatures import *


reader = DBReader('../db/github.2012_4_12.2012_8_14.db')
collab = reader.collaborators()
uid = reader.uid()

Gcollab = get_db_graph(Graph.COLLAB, uid, collab)

follow = reader.followers()
Gfollow = get_db_graph(Graph.COLLAB, uid, follow)

pull = reader.pull()
Gpull = get_db_graph(Graph.COLLAB, uid, pull)

watch = reader.watch()
Gwatch = get_db_graph(Graph.COLLAB, uid, watch)

print(consolidate_features(Gcollab, Gfollow, Gpull, Gwatch))
