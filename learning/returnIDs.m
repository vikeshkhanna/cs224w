function v= returnIDs(pageranks, mapping)
	% work with the first column of the F matrix which contains oldID to newID mapping
	[sortedPR, PRindex]= sort(pageranks);
	n_nodes= size(PRindex);
	topIDs= zeros(n_nodes);
	for i= 1:n_nodes
		topIDs= mapping(PRindex(i))
	% topIDs contains the old IDs of nodes to which source vertex is most likely to form edges, in order
