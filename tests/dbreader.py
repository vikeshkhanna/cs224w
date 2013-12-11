import path
from db.interface import * 
from analysis import graphutils
import utils

db = utils.get_small_db()
reader = DBReader(db)

uid = reader.uid()
rowid = uid.values()[0]
print reader.get_users([rowid, rowid])

Gcollab = graphutils.get_collab_graph(db, uid)
feature_graphs = graphutils.get_feat_graphs(db, uid)

base_graphs = graphutils.get_base_dict(Gcollab, feature_graphs)
graphutils.print_stats(base_graphs)

