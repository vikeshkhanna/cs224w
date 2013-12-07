% takes in the source node id, the mapping from v to phi(source, v), and the adjacency matrix A. Returns the sparse matrix Q.
% also takes in the model from the learning phase to calculate f(w, phi(u, v))

function Q= getQ(fname, beta)
	load(strcat(fname, "_RWfeatures.mat"));
	load(strcat(fname, "_model.mat"));
	% now matrices in memory should be Ai, Aj, Av (sparse matrix vectors), F (feature matrix with the first column being the node IDs for v and rest being features, and s which is the node ID of source node
	% the mapping from actual IDs to new IDs is: F(newID, 1)= oldID
	[n_nodes, n_features]= size(F);
	n_features= n_features-1; 	
	A= sparse(Ai, Aj, Av);
	n_edges= size(Ai);
	% find new ID for source node
	newSourceID= find(squeeze(F(:, 1))== s);
	% for every other node find f(w, phi(u, v))
	func= zeros(n_nodes, 1);
	for i= 1:n_nodes
		func(i)= calcFunc(squeeze(F(i, 2:end)), model, beta);
	end
	% now given the f(w, phi(s, v)) for every node v, calculate unnormalized values for Q based on A: for every edge (i, j) in A, assign it the weight func(j) 
	Qv= zeros(n_edges, 1);
	for e=1:n_edges
		% assign weight to only to edge (Ai(e), Aj(e)) 
		Qv(e)= func(Aj(e)); 
	end
	
	% now normalize Q- get sum over all neighbors j for a given i- so find normalizer(i)
	normalizer= zeros(n_nodes);
	for e = 1:n_edges
		normalizer(Ai(e))= normalizer(Ai(e)) + Qv(e);
	end
	
	% now normalize all the Qv values
	for e= 1:n_edges
		Qv(e)= Qv(e)/ normalizer(Ai(e));
	end
	
	Q= sparse(Ai, Aj, Qv);

