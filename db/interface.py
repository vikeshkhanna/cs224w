import sqlite3
import os

class DBBase:
	def __init__(self, db_file):
		self.db_file = os.path.abspath(db_file)
		self.conn = self.connect()

	def connect(self):
		return sqlite3.connect(self.db_file)

	def commit(self):
		self.conn.commit()

	def close(self):
		self.conn.close()

	def __exit__(self):	
		try:
			self.close()
		except:
			pass

class DBWriter(DBBase):
	DB_FILE='github.db'
	CREATE_FILE='create.sql'

	# returns the tuple - (userid, location)
	def get_user(self, userid):
		s = "SELECT * FROM user WHERE userid=?"
		ids = (userid,)
		self.conn.execute(s, ids)
		cur = self.conn.cursor()
		retVal = cur.fetchone()
		cur.close()
		return retVal

	# Idempotent - Only adds a user if not already present
	# login, location
	def add_user(self, user):
		ret_val = None

		userid = user['login']
		location = (user['location'] if "location" in user else None)
		
		row = (userid, location)
		comm = "INSERT OR IGNORE INTO user VALUES (?,?)"
		self.conn.execute(comm, row)
		ret_val = self.get_user(userid)
		return ret_val

	# tuple(userid1, userid2, created_at)
	def add_followers(self, follows):
		user1 = self.make_user(follows[0])
		user2 = self.make_user(follows[1])

		self.add_user(user1)
		self.add_user(user2)
		
		row = (follows[0], follows[1], follows[2])
		comm = "INSERT OR IGNORE INTO follows VALUES(?,?,?)"
		self.conn.execute(comm, row)	
	

	# repo object
	def add_repo(self, repo):
		language = repo['language'] if 'language' in repo else None
		description = repo['description'] if 'description' in repo else None

		row = (repo['owner'], repo['name'], repo['watchers'], repo['forks'], language, description, repo['created_at'])

		comm = "INSERT OR IGNORE INTO repository VALUES(?,?,?,?,?,?,?)"
		self.conn.execute(comm, row)		
		
	# userid = id of user who was added as member	
	def add_collab(self, userid, repo, created_at):
		# First add le repo
		self.add_user(self.make_user(userid))
		self.add_repo(repo)
		row = (userid, repo['name'], created_at)

		comm = "INSERT OR IGNORE INTO collaborate VALUES(?,?,?)"
		self.conn.execute(comm, row)
	
	def add_watch(self, userid, repo, created_at):
		# First add le repo
		self.add_user(self.make_user(userid))
		self.add_repo(repo)
		row = (userid, repo['name'], created_at)

		comm = "INSERT OR IGNORE INTO watch VALUES(?,?,?)"
		self.conn.execute(comm, row)
	
	def add_pull(self, userid, repo, status, created_at):
		# First add le repo
		self.add_user(self.make_user(userid))
		self.add_repo(repo)

		row = (userid, repo['name'], status, created_at)

		comm = "INSERT OR IGNORE INTO pull VALUES(?,?,?, ?)"
		self.conn.execute(comm, row)
	
	def add_fork(self, userid, repo, created_at):
		# First add le repo
		self.add_user(self.make_user(userid))
		self.add_repo(repo)

		row = (userid, repo['name'], created_at)

		comm = "INSERT OR IGNORE INTO fork VALUES(?,?,?)"
		self.conn.execute(comm, row)
	
	def add_issue(self, userid, repo, created_at):
		# First add le repo
		self.add_user(self.make_user(userid))
		self.add_repo(repo)

		row = (userid, repo['name'], created_at)

		comm = "INSERT OR IGNORE INTO issue VALUES(?,?,?)"
		self.conn.execute(comm, row)
	
	def make_user(self, login, location=None):
		return {"login":login, "location":location}

class DBReader(DBBase):
	pass	
		
	def collaborators(self):
		comm = "SELECT * from collaborate";
		return self.conn.execute(comm).fetchall()

	def followers(self):
		comm = "SELECT * from follows";
		return self.conn.execute(comm).fetchall()

	# returns the cursor
	def execute(self, comm):
		return self.conn.execute(comm)

