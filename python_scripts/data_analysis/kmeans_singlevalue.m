X = csvread('temp3.csv');
%hist(X);
[idx, C, sumd] = kmeans(X, 2, 'Distance', 'sqEuclidean', 'Display', 'final', 'Replicates', 5);
[silh,h] = silhouette(X, idx);
c = mean(silh);