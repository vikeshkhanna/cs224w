% takes in the _features and _ytrain matrix and outputs the _theta matrix
%function model = training(fname)
function model = training(features, ytrain)
    
    % standardization scale each features to unit variance and zero mean
    n_features = size(features, 2);
    fx = features;
    
    for i=1:n_features
        fx(:,i) = fx(:,i) - mean(fx(:,i));
    end;
    
    for i=1:n_features
        fx(:,i) = fx(:,i)/std(fx(:,i));
    end;
   
    m = size(fx, 1);
	% convert the 0-1 train matrix to 1-2 

    for i=1:m
        if(ytrain(i)==0)
                ytrain(i)=1;
        else 
                ytrain(i)=2;
        end
    end
 
    model = mnrfit(fx, ytrain);
    save 'model.mat' model; 
end
