% make script accept basename and source vertex ID
function topIDs = runRW(Ai, Aj, Av, F, src, beta)
	load('model.k4.mat')
	Q = getQ(Ai, Aj, Av, F, src, beta, model);
	p= getPageRanks(Q);
	[sortedp, topIDs]= sort(p, 'descend');
%	topIDs= returnIDs(p, mapping);
