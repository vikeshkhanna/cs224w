function pr= getPageRanks(Q)
	Q_t= Q';
	[n_nodes, ~]= size(Q);
	size(Q)
	pr= ones(n_nodes, 1)*1/n_nodes;
	old_pr= zeros(n_nodes, 1);
	epsilon= 0.01;
	while(convergence(pr, old_pr, epsilon)==0)
		fprintf('size of pr= %d', numel(pr))
		old_pr= pr;
		pr= Q_t * pr;
		fprintf('size of pr= %d', numel(pr))
	end
	
