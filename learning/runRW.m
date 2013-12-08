% make script accept basename and source vertex ID
function topIDs = runRW(Ai, Aj, Av, F, src, beta)
	load('model.mat')
    save 'runRW.debug.mat'
    
	Q = getQ(Ai, Aj, Av, F, src, beta, model);
	epsilon= 0.1;
	p= getPageRanks(Q, epsilon);
	[sortedp, topIDs]= sort(p, 'descend');
%	topIDs= returnIDs(p, mapping);
