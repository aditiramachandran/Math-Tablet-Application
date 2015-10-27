% performs k means clustering on denied/automatic hints
% navigate to Math-Tablet-Application/python_scripts/data_analysis

% denied_auto_hints.csv is the output of denied_auto_hints_extraction.py
% contains aggregate denied/auto hints across sessions for each participant
X = csvread('denied_auto_hints.csv');

% comment this section out if we do not want to use the means of both
% features to normalize the matrix
% divisors = mean(X);
% [nrows, ncols] = size(X);
% divisors = repmat(divisors, nrows, 1);
% X = X ./ divisors;

% idx is a vector of assigned cluster IDs, C contains the positions of the
% centroids, and sumd contains the summed distances of points to the
% centroids
[idx, C, sumd] = kmeans(X, 4);
figure;
% plots clusters with different colors
plot(X(idx==1,1),X(idx==1,2),'r.','MarkerSize',25)
hold on
plot(X(idx==2,1),X(idx==2,2),'b.','MarkerSize',25)
plot(X(idx==3,1),X(idx==3,2),'g.','MarkerSize',25)
plot(X(idx==4,1),X(idx==4,2),'c.','MarkerSize',25)

% plots centroids
plot(C(:,1),C(:,2),'kx',...
     'MarkerSize',15,'LineWidth',3)
legend('Cluster 1','Cluster 2','Cluster 3', 'Cluster 4','Centroids')
title 'Denied/Auto hints kmeans'
xlabel 'Denied Hints'
ylabel 'Auto Hints'
hold off
