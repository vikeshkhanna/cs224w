import sys
from db.interface import *
from learning import interface
from analysis import graphutils
from learning import consolidateFeatures

def main(args):
	db = args[0]
	date1 = args[1]
	date2 = args[2]


	reader = DBReader(db)
	print("Getting uid")
	uid = reader.uid()

	print("Getting Collab delta")
	collab_delta = reader.collaborators(date1, date2)
	reader.close()

	print("Getting all the base graphs")
	base_graphs = graphutils.get_db_graphs(db, uid, None, date1)
	print base_graphs["Gcollab"].GetNodes()

	print("Getting Gcollab delta graphs")
	Gcollab_delta = graphutils.get_db_graph(graphutils.Graph.COLLAB, uid, collab_delta) 

	features = consolidateFeatures.consolidate_features(**base_graphs)
	labels = consolidateFeatures.consolidate_labels(features, Gcollab_delta)
	interface.write(features, labels, "learning/data.mat", "github_train", "github_labels")

# base graph = till date1
# delta graph = date1 to date2

if __name__=="__main__":
	if len(sys.argv)<4:
		print("Usage: program.py <db> <date1> <date2>")
		sys.exit(1)
	
	main(sys.argv[1:])
