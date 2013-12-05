select distinct A.userid, B.userid 
from collaborate A, collaborate B 
where 
A.repo_name=B.repo_name and A.userid<B.userid

union

select distinct userid, owner 
from collaborate, repository
where collaborate.repo_name = repository.name;

