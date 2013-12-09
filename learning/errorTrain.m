function [fp_ep, fp_en, fn_ep, fn_en]= errorTrain(f, pihat, labels)
%ERROR Summary of this function goes here
%   Detailed explanation goes here
    %samples = size(labels, 1);
    [sortedpi, indices]= sort(pihat(:, 2), 'descend');
    disp(sortedpi)
    sortedlabels= zeros(numel(indices), 1);
    for i= 1:numel(indices)
        sortedlabels(i)= labels(indices(i));
    end
    %disp(sortedlabels)
    l= numel(sortedlabels);
    %fprintf('l is %d', l)
    s1= sum(sortedlabels(1:int64(l/4)))
    s2= sum(sortedlabels(int64(l/4): int64(l/2)))
    s3= sum(sortedlabels(int64(l/2): int64(3*l/4)))
    s4= sum(sortedlabels(int64(3*l/4): end))
    
    disp(s1)
    disp(s2)
    disp(s3)
    disp(s4)
    fp_ep=0;
    fn_ep=0;
    fp_en=0;
    fn_en=0;
    for i=1:l
        if labels(i)==1
            if sum(f(i, :))== -3
                fn_ep=fn_ep + 1;
            else
                fp_ep= fp_ep +1;
            end
        else
            if sum(f(i, :))== -3
                fn_en= fn_en+1;
            else
                fp_en= fp_en+1;
            end
        end
        
       
    end
    s= fp_en + fp_ep + fn_en + fn_ep;
    fp_en= fp_en/s;
    fp_ep= fp_ep/s;
    fn_en= fn_en/s;
    fn_ep= fn_ep/s;
end

