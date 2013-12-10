% takes in the source node id, feature matrix F , and the adjacency matrix A, and the model learnt from the learning stage. Returns the sparse matrix Q.
 
function Q = getQ(Ai, Aj, Av, F, src, beta, model)
	[n_nodes, n_features]= size(F);
	A= sparse(double(Ai), double(Aj), double(Av));
	Qi = Ai;
	Qj = Aj;
	
	n_edges= size(Ai, 1);	% not the actual number of edges
	% for every other node find f(w, phi(u, v))
	func= zeros(n_nodes, 1);
	for i= 1:n_nodes
		func(i)= calcFunc(squeeze(F(i, :)), model, beta);
	end
	% now given the f(w, phi(s, v)) for every node v, calculate unnormalized values for Q based on A: for every edge (i, j) in A, assign it the weight func(j) 
	Qv= zeros(n_edges, 1);

	for e=1:n_edges
		% assign weight to only to edge (Ai(e), Aj(e)) 
		Qv(e)= func(Aj(e)); 
	end
	
	% now normalize Q- get sum over all neighbors j for a given i- so find normalizer(i)
	normalizer= zeros(n_nodes, 1);
	for e = 1:n_edges
		normalizer(Ai(e))= normalizer(Ai(e)) + Qv(e);
	end
	% now normalize all the Qv values
	for e= 1:n_edges
		Qv(e)= Qv(e)/ normalizer(Ai(e));
	end
	
	Q = sparse(double(Ai), double(Aj), double(Qv));

	% Restart
	ALPHA = 0.3;
	Q = (1-ALPHA)*Q;
	Q(:, src) = Q(:,src) + ALPHA;
