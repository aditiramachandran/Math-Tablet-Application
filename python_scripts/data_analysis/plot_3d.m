X = csvread('3doutput.csv');

[idx, C, sumd] = kmeans(X, 3, 'Distance', 'sqEuclidean', 'Display', 'final', 'Replicates', 5);
figure;
% plots clusters with different colors
scatter3(X(idx==1,1),X(idx==1,2),X(idx==1,3));
hold on;
scatter3(X(idx==2,1),X(idx==2,2),X(idx==2,3));
scatter3(X(idx==3,1),X(idx==3,2),X(idx==3,3));
scatter3(X(idx==4,1),X(idx==4,2),X(idx==4,3));
%scatter3(X(idx==5,1),X(idx==5,2),X(idx==5,3));
%scatter3(X(idx==6,1),X(idx==6,2),X(idx==6,3));
%scatter3(X(idx==7,1),X(idx==7,2),X(idx==7,3));

s = scatter3(C(:,1),C(:,2),C(:,3));
s.Marker = '*';
%s.LineWidth = 5;

%legend('Cluster 1','Cluster 2','Cluster 3','Centroids');
%title 'always increasing c vals'
xlabel 'Denied Hints'
ylabel 'Auto Hints'
zlabel 'Time Until Hint1'
hold off

figure;
[silh,h] = silhouette(X, idx);
h = gca;
h.Children.EdgeColor = [.8 .8 1];
xlabel 'Silhouette Value';
ylabel 'Cluster';

% calculates accuracy of silhouette model
c = mean(silh);