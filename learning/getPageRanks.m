function pr = getPageRanks(Q, epsilon)
	save 'getPageRanks.debug.mat'
	
	Q_t= Q';
	[n_nodes, ~]= size(Q);
	size(Q)
	pr= ones(n_nodes, 1)*1/n_nodes;
	old_pr= zeros(n_nodes, 1);

	while(norm(pr- old_pr) > norm(pr) * epsilon)
        error = norm(pr-old_pr);
        tolerance = norm(pr)*epsilon;
        fprintf('error = %f\n', error);
        fprintf('Tolerance = %f, Ratio = %f\n', tolerance, error/norm(pr)); 
        old_pr= pr;
	pr = Q_t * pr;
	end
	
