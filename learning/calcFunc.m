function f= calcFunc(features, model, beta)
	% first find the probability of 1 from mnrval
	pihat= mnrval(model, features);

	%disp(features)
	p= pihat(2);	% p is probability of edge forming based on the features
	f= exp(beta*p);
end
	
