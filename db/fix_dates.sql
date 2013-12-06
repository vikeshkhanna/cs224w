update follows set created_at = rtrim(replace(created_at, '/', '-'),' -0700') where julianday(created_at) is NULL;
update collaborate set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
update repository set created_at = rtrim(replace(created_at, '/','-'), ' -0700') where julianday(created_at) is NULL;

update pull set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
update pull set created_at = replace(created_at,' -0700',':') where julianday(created_at) is NULL;

update issue set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
update fork set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
update watch set created_at = rtrim(replace(created_at, '/','-'),' -0700') where julianday(created_at) is NULL;
