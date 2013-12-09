function [s1, s2]= errorTrain(f, pihat, labels)
%ERROR Summary of this function goes here
%   Detailed explanation goes here
    %samples = size(labels, 1);
    [sortedpi, indices]= sort(pihat(:, 1), 'descend');
    disp(sortedpi)
    sortedlabels= zeros(numel(indices), 1);
    for i= 1:numel(indices)
        sortedlabels(i)= labels(indices(i));
    end
    %disp(sortedlabels)
    l= numel(sortedlabels);
    %fprintf('l is %d', l)
    s1= sum(sortedlabels(1:int64(l/4)));
    s2= sum(sortedlabels(int64(l/4): int64(l/2)));
    s3= sum(sortedlabels(int64(l/2): int64(3*l/4)));
    s4= sum(sortedlabels(int64(3*l/4): end));
    
    disp(s1)
    disp(s2)
    disp(s3)
    disp(s4)
    
    for i=1:l
        if labels(i)==1
            disp(f(i,:))
        end
        
        pause(0.5);
    end
end

