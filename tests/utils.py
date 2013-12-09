import path
from db import *
from analysis.graphutils import *

''' Helper functions for ease of use'''
def get_small_db():
	db = "../db/github.2012_4_12.2012_6_17.db"
	return db

def get_small_collab(min_date=None, max_date=None):
	db = get_small_db()
	reader = DBReader(db)
	uid = reader.uid()
	collab = reader.collaborators(min_date, max_date)
	Gcollab = get_db_graph(Graph.COLLAB, uid, collab)
	return Gcollab

def small_date1():
	return "2012-05-17"

def small_date2():
	return "2012-06-17"
