% make script accept basename and source vertex ID
function topIDs = runRW(Ai, Aj, Av, F, src, beta)
	load('model.mat')
<<<<<<< HEAD
    save 'runRW.debug.mat'
=======
    	save 'runRW.debug.mat'
    
>>>>>>> 2c8df402e5a225492e01a52facc117e8870016a3
	Q = getQ(Ai, Aj, Av, F, src, beta, model);
	p= getPageRanks(Q);
	[sortedp, topIDs]= sort(p, 'descend');
%	topIDs= returnIDs(p, mapping);
