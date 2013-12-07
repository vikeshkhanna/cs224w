function c= convergence(pr, old_pr, epsilon)
	disp(norm(pr-old_pr))
	disp(norm(pr))
	if(norm(pr-old_pr) > norm(pr) * epsilon)
		c= 0;
	else
		c= 1;
	end
