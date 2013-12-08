SELECT * FROM materialized;

DROP TABLE IF EXISTS gcollab;
DROP TABLE IF EXISTS materialized;
DROP TABLE IF EXISTS gpull;
DROP TABLE IF EXISTS gfork;
DROP TABLE IF EXISTS gwatch;

--Min date for gcollab and pull since they are not feature graphs. We should take the earliest edge that was formed. Other graphs have a single edge per node pair anyway

CREATE TABLE IF NOT EXISTS gcollab(userid1, userid2, created_at, score, unique(userid1, userid2));
INSERT OR IGNORE INTO gcollab SELECT * FROM (SELECT A.userid, B.userid, min(A.created_at, B.created_at) created_at, 0 from collaborate A, collaborate B where A.repo_id=B.repo_id and A.userid<B.userid group by A.userid, B.userid union select C.userid, R.owner, C.created_at, 1 from collaborate C, repository R where C.repo_id=R.name group by C.userid, R.owner);


CREATE TABLE IF NOT EXISTS gpull(userid1, userid2, created_at, score, unique(userid1, userid2));
INSERT OR IGNORE INTO gpull SELECT * FROM (select A.actor, B.actor, min(A.created_at, B.created_at) created_at, 0 from pull A, pull B where A.repo_id = B.repo_id and A.actor < B.actor group by A.actor, B.actor union SELECT actor, owner, pull.created_at created_at, 1 from pull, repository where pull.repo_id = repository.repo_id group by actor, owner);

-- max(created_at) because the edge is formed when the later of the two watches the common repo

CREATE TABLE IF NOT EXISTS gwatch(userid1, userid2, created_at, score, unique(userid1, userid2));
INSERT OR IGNORE INTO gwatch SELECT * FROM (select A.actor, B.actor, max(A.created_at, B.created_at) created_at, 0 from watch A, watch B where A.repo_id = B.repo_id and A.actor < B.actor group by A.actor, B.actor union SELECT actor, owner, watch.created_at created_at, 1 from watch, repository where watch.repo_id = repository.repo_id group by actor, owner);

--INSERT OR IGNORE INTO gwatch SELECT actor, owner, watch.created_at, 1 from watch, repository where watch.repo_id = repository.repo_id;

-- max(created_at) because the edge is formed when the later of the two forks the common repo

CREATE TABLE IF NOT EXISTS gfork(userid1, userid2, created_at, score, unique(userid1, userid2));
INSERT OR IGNORE INTO gfork SELECT * FROM (SELECT A.actor, B.actor, max(A.created_at, B.created_at) created_at, 0 from fork A, fork B where A.repo_id = B.repo_id and A.actor < B.actor group by A.actor, B.actor union SELECT actor, owner, fork.created_at, 1 from fork, repository where fork.repo_id = repository.repo_id group by actor, owner);

create table materialized(A);
insert into materialized values(1);





