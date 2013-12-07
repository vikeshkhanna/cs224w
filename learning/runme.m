% make script accept basename and source vertex ID
load(strcat(fname, '_srcFeatures.mat'));
load(strcat(fname, '_model.mat'));
load(strcat(fname, '_adjmat.mat'));	% or integrate with first file

mapping= F(:, 1);	% contains mapping from old IDs to new IDs
newAi= Ai;
newAj= Aj;
for i= 1:numel(Ai)
	newAi(i)= find(mapping==Ai(i));
	newAj(i)= find(mapping==Aj(i));
 
newSrcID= find(mapping==src);
Q= getQ(newAi, newAj, Av, F(:, 2:end), newSrcID, model);
epsilon= 0.01;
p= getPageRank(Q, epsilon);
topIDs= returnIDs(p, mapping);
% now find a way to return the topIDs to python
