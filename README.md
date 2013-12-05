This is the CS224W Fall 2013 project on link recommendation in GitHub. 

To create data - 
1. cd db
2. Run sqlite3 test.db < create.sql

To load data into db
1. python load.py -date1:2012-10-04-00 -date2:2012-04-12 -db:db/test.db -stream:online

To generate edge lists
1. cd analysis
2. ./gengraphs.sh ../db/test.db false

Setting the second argument to true above will also plot the graphs

To get graph properties
Prereq - Must have edge lists ready - See how to generate edge lists
1. python properties.py ../data/collaborators.out

