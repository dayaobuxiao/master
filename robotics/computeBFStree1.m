function [tree,parentvector] = computeBFStree(AdjTable,start)

sizeoftable = size(AdjTable);
numberofvert = sizeoftable(2);
for i=1:numberofvert
    vert(i)=i;
end
Q =[];
Q = [Q vert(start)];
for i=1:numberofvert
    parent(vert(i)) = 0;
end
parent(vert(start)) = vert(start);

tree = [];
parentvector = 0;
while ~isempty(Q)
    v = Q(1);
    tree = [tree Q(1)];
    Q(1)=[];
    n = size(AdjTable{v}(1,:));
    for j=1:n(2)
        u = AdjTable{v}(1,j);
        if parent(u) == 0
            parent(u) = v;
            Q = [Q u];
            parentvector= [parentvector v];
        end
    end
end
parentvector
end
