function f= calcFunc(features, model, beta)
	% first find the probability of 1 from mnrval
	pihat= mnrval(model, features);
<<<<<<< HEAD
	%disp(features)
	p= pihat(2);	% p is probability of edge forming based on the features
	f= exp(beta*p);
=======
	p = pihat(2);	% p is probability of edge forming based on the features
	f = exp(beta*p);
	disp(features);
>>>>>>> 2c8df402e5a225492e01a52facc117e8870016a3
end
	
