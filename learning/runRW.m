% make script accept basename and source vertex ID
function topIDs = runRW(Ai, Aj, Av, F, src, beta)
	disp('Random Walk starteth.')
	load('model.mat')
	Q = getQ(Ai, Aj, Av, F, src, beta, model);
	p= getPageRanks(Q);
	[sortedp, topIDs]= sort(p, 'descend');
%	topIDs= returnIDs(p, mapping);
