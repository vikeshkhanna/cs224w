create table user(
	userid text PRIMARY KEY, 
	location text default NULL
);

create table follows(
	userid1 text,
	userid2 text,
	created_at datetime NOT NULL,
	constraint fk_follows_id1 foreign key(userid1) references user(userid),
	constraint fk_follows_id2 foreign key(userid2) references user(userid)
);

create table repository(
	owner text,
	name text PRIMARY KEY, 
	watchers number NOT NULL DEFAULT 0,
	forks number NOT NULL DEFAULT 0,
	language text,
	description text,
	created_at datetime NOT NULL,
	constraint fk_repository_owner foreign key(owner) references user(userid)
);

create table collaborate(
	userid text, 
	repo_name text,
	created_at datetime NOT NULL,
	constraint fk_collaborate_id foreign key(userid) references user(userid),
	constraint fk_collaborate_repo foreign key(repo_name) references repository(repo_name)
);

create table pull(
	actor text, 
	repo_name text, 
	status text NOT NULL,
	created_at datetime NOT NULL,
	constraint fk_pull_userid foreign key(actor) references user(userid),
	constraint fk_pull_repo foreign key(repo_name) references repository(name)
);

create table issue(
	actor text,
	repo_name text,
	status text NOT NULL,
	created_at datetime NOT NULL,
	constraint fk_issue_userid foreign key(actor) references user(userid),
	constraint fk_issue_repo foreign key(repo_name) references repository(name)
);

create table fork(
	actor text,
	repo_name text,
	created_at datetime NOT NULL,
	constraint fk_issues_userid foreign key(actor) references user(userid)
);

create table watch(
	actor text,
	repo_name text,
	created_at datetime NOT NULL,
	constraint fk_watch_userid foreign key(actor) references user(userid)
);
