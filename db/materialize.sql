SELECT * FROM materialized;

CREATE TABLE IF NOT EXISTS gcollab(userid1, userid2, created_at, score);
INSERT OR IGNORE INTO gcollab SELECT * FROM (SELECT A.userid, B.userid, max(A.created_at, B.created_at) created_at, 0 from collaborate A, collaborate B where A.repo_name=B.repo_name and A.userid<B.userid union select C.userid, R.owner, C.created_at, 1 from collaborate C, repository R where C.repo_name=R.name);


CREATE TABLE IF NOT EXISTS gpull(userid1, userid2, created_at, score);
INSERT OR IGNORE INTO gpull SELECT * FROM (select A.actor, B.actor, max(A.created_at, B.created_at) created_at, 0 from pull A, pull B where A.repo_name = B.repo_name and A.actor < B.actor union SELECT actor, owner,pull.created_at created_at, 1 from pull, repository where pull.repo_name = repository.name);


CREATE TABLE IF NOT EXISTS gwatch(userid1, userid2, created_at, score);
INSERT OR IGNORE INTO gwatch SELECT actor, owner, watch.created_at, 1 from watch, repository where watch.repo_name = repository.name;

CREATE TABLE IF NOT EXISTS gfork(userid1, userid2, created_at, score);
INSERT OR IGNORE INTO gfork SELECT * FROM (SELECT A.actor, B.actor, max(A.created_at, B.created_at) created_at, 0 from fork A, fork B where A.repo_name = B.repo_name and A.actor < B.actor union SELECt actor, owner, fork.created_at, 1 from fork, repository where fork.repo_name = repository.name);

create table materialized(A);
insert into materialized values(1);





