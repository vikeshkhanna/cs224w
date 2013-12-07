% takes in the _features and _ytrain matrix and outputs the _theta matrix
%function model = training(fname)
function model = training(features, ytrain)
	m = size(features, 1);
	% convert the 0-1 train matrix to 1-2 

    for i=1:m
        if(ytrain(i)==0)
                ytrain(i)=1;
        else 
                ytrain(i)=2;
        end
    end
 
	model = mnrfit(features, ytrain);
	%save strcat("xx", "_model.mat") model 
end
