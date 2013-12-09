function pr = getPageRanks(Q)
	save 'getPageRanks.debug.mat'
	
	Q_t= Q';
	[n_nodes, ~]= size(Q);
	pr= ones(n_nodes, 1)*1/n_nodes;
	old_pr= zeros(n_nodes, 1);
	max_iterations = 100;
	iter = 0;
	epsilon = 0.1;

	while(norm(pr- old_pr) > norm(pr) * epsilon && iter <= max_iterations)
		error = norm(pr-old_pr);
		tolerance = norm(pr)*epsilon;
		%fprintf('error = %f\n', error);
		%fprintf('Tolerance = %f, Ratio = %f\n', tolerance, error/norm(pr)); 
		old_pr = pr;
		pr = Q_t * pr;
		iter = iter + 1;
	end
end
