.output pull.out

select actor, owner, count(*) as number_of_requests
from pull, repository 
where pull.repo_name = repository.name and actor!=owner
group by actor, owner;
