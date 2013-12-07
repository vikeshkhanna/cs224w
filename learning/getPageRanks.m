function pr= getPageRanks(Q)
	Q_t= Q';
	n_nodes= size(Q);
	pr= zeros(n_nodes, 1);
	old_pr= ones(n_nodes, 1);
	while(convergence(pr, old_pr)==0)
		old_pr= pr;
		pr= Q_t * pr;
	end
	
