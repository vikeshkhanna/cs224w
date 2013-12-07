create table user(
	userid text PRIMARY KEY, 
	location text default NULL
);

--Indexes
create index if not exists index_user_id on user(userid);

create table follows(
	userid1 text,
	userid2 text,
	created_at datetime NOT NULL,
	constraint fk_follows_id1 foreign key(userid1) references user(userid),
	constraint fk_follows_id2 foreign key(userid2) references user(userid),
	unique(userid1, userid2) on conflict ignore
);

create index if not exists index_follow_id on follows(userid1);

create table repository(
	repo_id integer PRIMARY KEY AUTOINCREMENT,
	owner text,
	name text, 
	watchers number NOT NULL DEFAULT 0,
	forks number NOT NULL DEFAULT 0,
	language text,
	description text,
	created_at datetime NOT NULL,
	constraint fk_repository_owner foreign key(owner) references user(userid),
	unique(owner, name) on conflict ignore
);

create index if not exists index_repository_name on repository(owner, name);
create index if not exists index_repository_name on repository(owner);
create index if not exists index_repository_name on repository(name);

create table collaborate(
	userid text, 
	repo_id integer, 
	created_at datetime NOT NULL,
	constraint fk_collaborate_id foreign key(userid) references user(userid),
	constraint fk_collaborate_repo_id foreign key(repo_id) references repository(repo_id),
	unique(userid, repo_id) on conflict ignore
);

create index if not exists index_collaborate_repo on collaborate(repo_id);

create table pull(
	actor text, 
	repo_id integer, 
	status text NOT NULL,
	created_at datetime NOT NULL,
	constraint fk_pull_userid foreign key(actor) references user(userid),
	constraint fk_pull_repo_id foreign key(repo_id) references repository(repo_id),
	unique(actor, repo_id, created_at) on conflict ignore
);

create index if not exists index_pull_repo on pull(repo_id);
create index if not exists index_pull_actor on pull(actor);

create table issue(
	actor text,
	repo_id integer,
	created_at datetime NOT NULL,
	constraint fk_issue_userid foreign key(actor) references user(userid),
	constraint fk_issue_repo_id foreign key(repo_id) references repository(repo_id),
	unique(actor, repo_id, created_at) on conflict ignore
);

create index if not exists index_issue_repo on issue(repo_id);
create index if not exists index_issue_actor on issue(actor);

create table fork(
	actor text,
	repo_id integer,
	created_at datetime NOT NULL,
	constraint fk_fork_userid foreign key(actor) references user(userid),
	constraint fk_fork_repo_id foreign key(repo_id) references repository(repo_id),
	unique(actor, repo_id) on conflict ignore
);

create index if not exists index_fork_repo on fork(repo_id);
create index if not exists index_fork_actor on fork(actor);

create table watch(
	actor text,
	repo_id integer,
	created_at datetime NOT NULL,
	constraint fk_watch_userid foreign key(actor) references user(userid),
	constraint fk_watch_repo_id foreign key(repo_id) references repository(repo_id),
	unique(actor, repo_id) on conflict ignore
);

create index if not exists index_watch_repo on watch(repo_id);
create index if not exists index_watch_actor on watch(actor);

create table duration(start_date datetime, end_date datetime);
