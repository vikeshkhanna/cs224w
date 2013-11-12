import sqlite3
import os

class DB:
	DB_FILE='github.db'
	CREATE_FILE='create.sql'

	def __init__(self, db):
		self.DB_PATH = os.path.abspath(db)
		self.CREATE_PATH = os.path.join(os.path.join(self.DB_PATH, os.pardir), DB.CREATE_FILE)

	def create(self):
		if not os.path.exists(self.DB_PATH):
			f = open(self.CREATE_PATH)
			commands = f.read().replace("\n","").replace("\t","").split(";")
			conn = self.conn()
			
			for comm in commands:
				conn.execute(comm)

	def connect(self):
		return sqlite3.connect(self.DB_PATH)

	# returns the tuple - (userid, location)
	def get_user(self, userid):
		conn = self.connect() 
		s = "SELECT * FROM user WHERE userid=?"
		ids = (userid,)
		cur = conn.cursor()
		cur.execute(s, ids)
		retVal = cur.fetchone()
		cur.close()
		conn.close()
		return retVal

	# Idempotent - Only adds a user if not already present
	# login, location
	def add_user(self, user):
		conn = self.connect()
		cur = conn.cursor()
		ret_val = None

		userid = user['login']
		location = (user['location'] if "location" in user else None)
		
		row = (userid, location)
		comm = "INSERT OR IGNORE INTO user VALUES (?,?)"
		cur.execute(comm, row)
		conn.commit()
		ret_val = self.get_user(userid)
			
		cur.close()
		conn.close()
		return ret_val

	# tuple(userid1, userid2, created_at)
	def add_followers(self, follows):
		user1 = self.make_user(follows[0])
		user2 = self.make_user(follows[1])

		self.add_user(user1)
		self.add_user(user2)
		
		conn = self.connect()
		cur = conn.cursor()
		
		row = (follows[0], follows[1], follows[2])
		comm = "INSERT OR IGNORE INTO follows VALUES(?,?,?)"
		cur.execute(comm, row)	
		conn.commit()

		cur.close()
		conn.close()			

	# repo object
	def add_repo(self, repo):
		language = repo['language'] if 'language' in repo else None
		description = repo['description'] if 'description' in repo else None

		row = (repo['owner'], repo['name'], repo['watchers'], repo['forks'], language, description, repo['created_at'])
		conn = self.connect()
		cur = conn.cursor()

		comm = "INSERT OR IGNORE INTO repository VALUES(?,?,?,?,?,?,?)"
		cur.execute(comm, row)		
		
		conn.commit()
		cur.close()
		conn.close()
	
	# userid = id of user who was added as member	
	def add_collab(self, userid, repo, created_at):
		# First add le repo
		self.add_repo(repo)
		row = (userid, repo['name'], created_at)

		conn = self.connect()
		cur = conn.cursor()
	
		comm = "INSERT OR IGNORE INTO collaborate VALUES(?,?,?)"
		cur.execute(comm, row)
		conn.commit()
	
		cur.close()
		conn.close()
	
	def make_user(self, login, location=None):
		return {"login":login, "location":location}
		
