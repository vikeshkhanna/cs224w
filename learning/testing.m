% accepts theta, feature matrix and outputs the _yestimate matrix
function testing(fname)
testfeatures= load(strcat(fname, "_testfeatures.mat"));
model= load(strcat(fname, "_model.mat"));
[m, n]= size(features);
ytest= zeros(m, 1);
% for every data point calculate y value
pihat= mnrfit(model, testfeatures);	
% now for pihat take the class corresponding to highest probability
for i= 1:m
	if(pihat(1) > pihat(2))
		ytest(i)= 0
	else
		ytest(i)= 1
save strcat(fname, "_ytest.mat") ytest
