import path
from learning import getFeatures
from db.interface import *
from analysis import graphutils

db = '../db/github.2013_1_20.2013_2_20.db'
reader = DBReader(db)
uid = reader.uid()

base_graphs = graphutils.get_db_graphs(db, uid)
Gcollab = base_graphs["Gcollab"]
feature_graphs = graphutils.split_feat_graphs(base_graphs)

reader.close()

start = Gcollab.GetRndNId()
walk_features = getFeatures.get_walk_features(Gcollab, feature_graphs, start)
print(walk_features)


