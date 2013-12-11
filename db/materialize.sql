SELECT "Dropping tables";

DROP TABLE IF EXISTS gcollab;
DROP TABLE IF EXISTS materialized;
DROP TABLE IF EXISTS gpull;
DROP TABLE IF EXISTS gfork;
DROP TABLE IF EXISTS gwatch;
DROP TABLE IF EXISTS gcollab_pull;

--Min date for gcollab and pull since they are not feature graphs. We should take the earliest edge that was formed. Other graphs have a single edge per node pair anyway
SELECT "Gcollab";

CREATE TABLE IF NOT EXISTS gcollab(userid1, userid2, created_at, score, jday, unique(userid1, userid2) on conflict ignore);
INSERT OR IGNORE INTO gcollab SELECT *, julianday(cdate) FROM (SELECT A.userid, B.userid, min(max(A.created_at, B.created_at)) cdate, 0 from collaborate A, collaborate B where A.repo_id=B.repo_id and A.userid<B.userid group by A.userid, B.userid union select C.userid, R.owner, min(C.created_at) cdate, 1 from collaborate C, repository R where C.repo_id=R.repo_id);

DROP INDEX IF EXISTS gcollab_jday;
CREATE INDEX gcollab_jday on gcollab(jday);

SELECT "Gpull";

CREATE TABLE IF NOT EXISTS gpull(userid1, userid2, created_at, score, jday, unique(userid1, userid2) on conflict ignore);
INSERT OR IGNORE INTO gpull SELECT *, julianday(cdate) FROM (select A.actor, B.actor, min(max(A.created_at, B.created_at)) cdate, 0 from pull A, pull B where A.repo_id = B.repo_id and A.actor < B.actor group by A.actor, B.actor union SELECT actor, owner, min(pull.created_at) cdate, 1 from pull, repository where pull.repo_id = repository.repo_id);

DROP INDEX IF EXISTS gpull_jday;
CREATE INDEX gpull_jday on gpull(jday);

-- max(created_at) because the edge is formed when the later of the two watches the common repo

SELECT "Gwatch";

CREATE TABLE IF NOT EXISTS gwatch(userid1, userid2, created_at, score, jday, unique(userid1, userid2) on conflict ignore);
INSERT OR IGNORE INTO gwatch SELECT actor, owner, watch.created_at cdate, count(*), julianday(watch.created_at) from watch, repository where watch.repo_id = repository.repo_id group by actor, owner;

DROP INDEX IF EXISTS gwatch_jday;
CREATE INDEX gwatch_jday on gwatch(jday);

-- max(created_at) because the edge is formed when the later of the two forks the common repo

SELECT "Gfork";

CREATE TABLE IF NOT EXISTS gfork(userid1, userid2, created_at, score, jday, unique(userid1, userid2) on conflict ignore);
INSERT OR IGNORE INTO gfork SELECT actor, owner, fork.created_at cdate, count(*), julianday(fork.created_at) from fork, repository where fork.repo_id = repository.repo_id group by actor, owner;

DROP INDEX IF EXISTS gfork_jday;
CREATE INDEX gfork_jday on gfork(jday);

SELECT "collab_pull";
CREATE TABLE IF NOT EXISTS gcollab_pull(userid1, userid2, created_at, score, jday, unique(userid1, userid2) on conflict ignore);
INSERT OR IGNORE INTO gcollab_pull SELECT *, julianday(cdate) FROM (SELECT userid1, userid2, min(created_at) cdate, score FROM (select * from gcollab union SELECT * FROM gpull) group by userid1, userid2);

DROP INDEX IF EXISTS gcollab_pull_jday;
CREATE INDEX gcollab_pull_jday on gcollab_pull(jday);

ALTER TABLE follows add column jday;
update follows set jday = julianday(created_at);

DROP INDEX IF EXISTS follows_jday;
create index follows_jday on follows(jday);

create table materialized(A);
insert into materialized values(1);

