import sys
import json
from db.interface import *

'''
@author: Vikesh Khanna
@notes: CS224W Final Project
'''

# Processors for various event types
# Receive json object in string form
# Process Method is passed to yajl helper to process streamed JSON
# Action method is called by the main script after collecting processing is complete
# Each processor has the events list for debugging. It can be removed later. 
# Do the jazz. 
class BaseProcessor:
	def __init__(self, db_file):
		self.db = DBWriter(db_file)
		self.cnt = 0

	def process(self, js):
		try:
			obj = json.loads(js)
			target_event = obj['type'].strip()

			if target_event in Event.Events:
				#print("Processing %s" % target_event)
				processor = Event.Processors[target_event](self.db)
				processor.process(obj)	
				processor.action()
				self.cnt+=1
			else:
				pass
		except:
			print("BaseProcessor ERROR: %s"%js)
			print(sys.exc_info())

	def action(self):
		print("Processed %d relevant events. Commiting changes."%self.cnt)
		self.db.commit()
		self.db.close()

	def __exit__(self, type, value, traceback):
		self.action()

# Prints a given number of json objects of the given type from the stream
class DebugProcessor:
	def __init__(self, target_event, cnt=1):
		self.count=cnt
		self.target_event = target_event

	def process(self, js):
		try:
			obj = json.loads(js)
			
			if obj['type'] == self.target_event and self.count > 0:
				print(json.dumps(obj, sort_keys=True, indent=5))
				self.count -= 1

				if self.count > 0:
					print("************")
		except:
			print("DebugProcessor ERROR: %s"%js)
			print(sys.exc_info()[0])

	def action(self):
		pass

class FollowProcessor:
	def __init__(self, db):
		self.follows = ()
		self.db = db
	def process(self, obj):
		try:
			user1 = obj["actor"]
			user2 =  obj["payload"]["target"]["login"]
			created_at = obj["created_at"]
			self.follows = (user1, user2, created_at)
		except:
			print("ERROR: %s"%str(obj))
			print(sys.exc_info())

	def action(self):
		# print self.follows
		self.db.add_followers(self.follows)

class MemberProcessor:
	def __init__(self, db):		
		# User A listed User B as collaborator
		self.db = db

	def process(self, obj):
		try:
			self.member = obj['payload']['member']['login']
			self.repo = obj['repository']
			self.created_at = obj['created_at']
		except:
			print("ERROR: %s"%str(obj))
			print(sys.exc_info())

	def action(self):
		#print self.collab
		self.db.add_collab(self.member, self.repo, self.created_at)		
		
class CreateProcessor: 
	def __init__(self, db):		
		# User A created a repository
		self.db = db

	def process(self, obj):
		try:
			self.repo = obj['repository']
		except:
			print("ERROR: %s"%str(obj))
			print(sys.exc_info()[0])

	def action(self):
		self.db.add_repo(self.repo)
			
class ForkProcessor:
	def __init__(self, db):		
		# User A created a repository
		self.db = db

	def process(self, obj):
		try:
			self.userid = obj['actor']
			self.repo = obj['repository']
			self.created_at = obj['created_at']
		except:
			print("ERROR: %s"%str(obj))
			print(sys.exc_info()[0])

	def action(self):
		self.db.add_fork(self.userid, self.repo, self.created_at)

class WatchProcessor:
	def __init__(self, db):		
		# User A created a repository
		self.db = db

	def process(self, obj):
		try:
			self.userid = obj['actor']
			self.repo = obj['repository']
			self.created_at = obj['created_at']
		except:
			print("ERROR: %s"%str(obj))
			print(sys.exc_info()[0])

	def action(self):
		self.db.add_watch(self.userid, self.repo, self.created_at)

class IssuesProcessor:
	def __init__(self, db):		
		# User A created a repository
		self.db = db

	def process(self, obj):
		try:
			self.userid = obj['actor']
			self.repo = obj['repository']
			self.created_at = obj['created_at']

		except:
			print("ERROR: %s"%str(obj))
			print(sys.exc_info()[0])

	def action(self):
		self.db.add_issue(self.userid, self.repo, self.created_at)

class PullRequestProcessor:
	def __init__(self, db):		
		# User A created a repository
		self.db = db

	def process(self, obj):
		try:
			self.userid = obj['actor']
			self.repo = obj['repository']
			self.status = obj['payload']['action']
			self.created_at = obj['created_at']
		except:
			print("ERROR: %s"%str(obj))
			print(sys.exc_info()[0])

	def action(self):
		self.db.add_pull(self.userid, self.repo, self.status, self.created_at)

class Event:
	FollowEvent = 'FollowEvent'
	CreateEvent = 'CreateEvent'
	ForkEvent = 'ForkEvent'
	WatchEvent = 'WatchEvent'
	IssuesEvent = 'IssuesEvent'
	MemberEvent = 'MemberEvent'
	PullRequestEvent = 'PullRequestEvent'

	# Must be in sync with above variables	
	Events = [FollowEvent, CreateEvent, ForkEvent, WatchEvent, IssuesEvent, MemberEvent, PullRequestEvent]

	# Must be in sync with function definitions below
	Processors = {FollowEvent: FollowProcessor, CreateEvent: CreateProcessor, ForkEvent: ForkProcessor, WatchEvent: WatchProcessor, IssuesEvent: IssuesProcessor, MemberEvent: MemberProcessor, PullRequestEvent: PullRequestProcessor}

