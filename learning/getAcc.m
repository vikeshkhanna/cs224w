% takes _ytest and _ytrain and returns accuracy
function getAcc(fname)
ytest= load((fname, "_ytest.mat"));
ytrain= load((fname, "_ytrain.mat"));
m= size(ytest, 1);
n= size(ytrain, 1);
if(m ~= n)
	fprintf("non matching dimensions")
end
true_positive=0;
true_negative=0;
false_positive=0;
false_negative=0;

for i= 1:m
	if(ytrain(i)==0)
		if(ytest(i)==0)
			true_negative= true_negative + 1;
		else
			false_positive= false_positive + 1;
		end
	else
		if(ytest(i)==0)
			false_negative= false_negative+1;
		else
			true_positive= true_positive + 1;
	end
end

recall= true_positive/ (true_positive + false_negative)
precision= true_positive/ (true_positive + false_positive)
accuracy= (true_positive + true_negative)/m

