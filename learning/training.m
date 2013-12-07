% takes in the _features and _ytrain matrix and outputs the _theta matrix
function training(fname)
	features= load(strcat(fname, "_features.mat"));
	ytrain= load(strcat(fname, "_ytrain"));
	[m, n] = size(features);
	% convert the 0-1 train matrix to 1-2 
	for i = 1:m
		if(ytrain(i)==0)
			ytrain(i)=1;
		else
			ytrain(i)=2;
	model= mnrfit(features, ytrain);
	save strcat(fname, "_model.mat") model 

