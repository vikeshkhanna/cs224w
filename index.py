import SimpleHTTPServer
from db.interface import *
from analysis import graphutils
import snappy.snap as snap
import snappy.snapext as snapext
from walk import runrw
from BaseHTTPServer import BaseHTTPRequestHandler
import SocketServer
import json
import sys

PORT = 8000

#db = "db/github.2012_4_12.2012_6_17.db"
db = "db/github.2013_9_12.2013_12_14.db"
date1 = "2013-12-14"

k=2
beta=12

reader = DBReader(db)
print("Getting uid")
uid = reader.uid()

print("Getting all the base graphs")

'''
Gcollab_base = graphutils.get_collab_graph(db, uid)
assert(Gcollab_base.IsNode(src))

feature_graphs = graphutils.get_feat_graphs(db, uid, None, date1)
base_graphs = graphutils.get_base_dict(Gcollab_base, feature_graphs)

# from base graph take a random source node in every iteration
baseG = base_graphs[graphutils.Graph.COLLAB]
featG = graphutils.split_feat_graphs(base_graphs)

'''
followers = reader.followers()
baseG = graphutils.get_db_graph(graphutils.Graph.FOLLOW, uid, followers)

#Gp = snapext.EUNGraph()
#featG = [Gp, Gp, Gp]

featG = graphutils.split_feat_graphs(graphutils.get_feat_graphs(db, uid, None, date1))

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def end_headers(self):
		self.send_head()
		SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

	def send_head(self):
		self.send_header("Content-type", "application/json")
		self.send_header("Access-Control-Allow-Origin", "*")
		
	def do_GET(self):

		try:
			userid = self.path.lstrip("/")

			if userid not in uid:
				return self.error(userid + " not in graph snapshot")

			src = uid[userid]
			
			if not baseG.IsNode(src):
				return self.error(userid + " not in graph snapshot")

			print("Creating subgraph")
			subBaseG = graphutils.getSubGraph(baseG, src, 4)
			print("Subgraph ready")

			topIDs = runrw.runrw(subBaseG, featG, src, beta)[:20]	
			cache = reader.get_users(topIDs)
			users = []
			print(cache)

			for rowid in cache:
				users.append(cache[rowid])
				
			self.send_response(200)
			self.end_headers()
	
			self.wfile.write(json.dumps(users))	
		except:
			self.wfile.write(sys.exc_info())

		return
	
	def error(self, msg):
		self.send_response(500)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		self.wfile.write(msg)
		return -1

Handler = RequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
