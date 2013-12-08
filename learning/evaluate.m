% accepts theta, feature matrix and outputs the _yestimate matrix
function [pihat, ytest] = evaluate(features, model)
	
	m = size(features, 1);
	ytest = zeros(m, 1);

	% for every data point calculate y value
	pihat = mnrval(model, features);	
    
	% now for pihat take the class corresponding to highest probability
	for i= 1:m
		if(pihat(1) > pihat(2))
			ytest(i) = 0;
		else
			ytest(i) = 1;
		end
	end
end

