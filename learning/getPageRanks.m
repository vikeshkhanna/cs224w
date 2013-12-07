function pr= getPageRanks(Q, epsilon)
	Q_t= Q';
	[n_nodes, ~]= size(Q);
	size(Q)
	pr= ones(n_nodes, 1)*1/n_nodes;
	old_pr= zeros(n_nodes, 1);
	while(norm(pr- old_pr) > norm(pr) * epsilon)
		fprintf('size of pr= %d', numel(pr))
		old_pr= pr;
		pr= Q_t * pr;
		fprintf('size of pr= %d', numel(pr))
	end
	
