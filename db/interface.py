import sqlite3
import os
import dateutil.parser
import datetime

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

class DBReadQuery:
	pass

class DBReader(DBBase):
	def uid(self):
		comm = "SELECT rowid, userid FROM user"
		rows = self.conn.execute(comm).fetchall()
		cache = {row[1]:row[0] for row in rows}
		return cache
		
	# Date format must be - YYYY-MM-DD HH:mm:ss
	def clip(self, rows, index, min_date, max_date):
		result = []

		if min_date!=None and max_date!=None:
			d1 = dateutil.parser.parse(min_date)
			d2 = dateutil.parser.parse(max_date)

			for row in rows:
				d = dateutil.parser.parse(row[index])
				d = d.replace(tzinfo=None)

				if d>=d1 and d<=d2:
					result.append(row)
		else:
			result = rows

		return result

	def dbclip(self, comm, min_date, max_date):
		suffix = ''

		if min_date!=None and max_date!=None:
			suffix = " WHERE julianday(created_at) >= julianday('%s') and julianday(created_at) <= julianday('%s')"%(min_date, max_date)
		elif min_date!=None:
			suffix = " WHERE julianday(created_at) >= julianday('%s')"%(min_date)
		elif max_date!=None:
			suffix = " WHERE julianday(created_at) <= julianday('%s')"%(max_date)

		return (comm + suffix)
		
	
	# Date format must be - YYYY-MM-DD HH:mm:ss
	def collaborators(self, min_date=None, max_date=None):
		comm = DBReadQuery.all_collaborators
		comm = self.dbclip(comm, min_date, max_date)	
		return self.conn.execute(comm).fetchall()
		#return self.clip(rows, 2, min_date, max_date)
	

	# Date format must be - YYYY-MM-DD HH:mm:ss
	def followers(self, min_date=None, max_date=None):
		comm = DBReadQuery.all_followers
		comm = self.dbclip(comm, min_date, max_date)
		return self.conn.execute(comm).fetchall()

	def pull(self, min_date=None, max_date=None):
		comm = self.dbclip(DBReadQuery.all_pull, min_date, max_date)
		return self.conn.execute(comm).fetchall()

	def watch(self, min_date=None, max_date=None):
		comm = self.dbclip(DBReadQuery.all_watch, min_date, max_date)
		return self.conn.execute(comm).fetchall()

	# returns the cursor
	def execute(self, comm):
		return self.conn.execute(comm)

# optimize
class DBReadQuery:
	'''
	all_collaborators = "SELECT * FROM (SELECT A.userid, B.userid, max(A.created_at, B.created_at) created_at from collaborate A, collaborate B where A.repo_name=B.repo_name and A.userid<B.userid union select C.userid, R.owner, C.created_at from collaborate C, repository R where C.repo_name=R.name)"
	all_followers = "SELECT * FROM follows"

	all_pull = "SELECT * FROM (select A.actor, B.actor, max(A.created_at, B.created_at) created_at, 0 from pull A, pull B where A.repo_name = B.repo_name and A.actor < B.actor union SELECT actor, owner,pull.created_at created_at, 1 from pull, repository where pull.repo_name = repository.name)"

	all_watch = "SELECT* FROM (SELECT A.actor, B.actor, max(A.created_at, B.created_at) created_at, 0 from watch A, watch B where A.repo_name = B.repo_name and A.actor < B.actor union SELECt actor, owner, watch.created_at, 1 from watch, repository where watch.repo_name = repository.name)"
	'''

	all_collaborators = "SELECT * from gcollab";
	all_pull = "SELECT * from gpull";
	all_followers = "SELECT *, 0 from follows";
	all_watch = "SELECT * from gwatch";
