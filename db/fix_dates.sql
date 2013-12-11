update follows set created_at = rtrim(replace(created_at, '/', '-'),' -0700') where julianday(created_at) is NULL;
update collaborate set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
update repository set created_at = rtrim(replace(created_at, '/','-'), ' -0700') where julianday(created_at) is NULL;

update pull set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
update pull set created_at = replace(created_at,' -0700',':') where julianday(created_at) is NULL;

update issue set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
update fork set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
update watch set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;


-- Something stupid has happened and some dates are like : 2012-05-12 17:16:5
-- Hack is to add a 0 first to make it 17:16:50... still some dates might be like 2012-05-12 16:15: - Add a zero again to dates that are null

update follows set created_at=created_at||0 where julianday(created_at) is null;
update follows set created_at=created_at||0 where julianday(created_at) is null;

update collaborate set created_at=created_at||0 where julianday(created_at) is null;
update collaborate set created_at=created_at||0 where julianday(created_at) is null;

update repository set created_at=created_at||0 where julianday(created_at) is null;
update repository set created_at=created_at||0 where julianday(created_at) is null;

update pull set created_at=created_at||0 where julianday(created_at) is null;
update pull set created_at=created_at||0 where julianday(created_at) is null;

update issue set created_at=created_at||0 where julianday(created_at) is null;
update issue set created_at=created_at||0 where julianday(created_at) is null;

update fork set created_at=created_at||0 where julianday(created_at) is null;
update fork set created_at=created_at||0 where julianday(created_at) is null;

update watch set created_at=created_at||0 where julianday(created_at) is null;
update watch set created_at=created_at||0 where julianday(created_at) is null;
