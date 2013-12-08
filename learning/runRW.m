% make script accept basename and source vertex ID
function topIDs= runRW(Ai, Aj, Av, F, src, model)
	Q= getQ(newAi, newAj, Av, F, src, model);
	epsilon= 0.01;
	p= getPageRank(Q, epsilon);
	[sortedp, topIDs]= sort(p);
%	topIDs= returnIDs(p, mapping);
