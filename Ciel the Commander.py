import sys

class Tree:
    def __init__(self, n):
        self.size = n + 1
        self.cur_size = 0
        self.tree = [[] for _ in range(self.size)]
        self.iscentroid = [False] * self.size
        self.ctree = [[] for _ in range(self.size)]
        self.characters=[None for _ in range(self.size)]
    
    def dfs(self, src, visited, subtree):
        visited[src] = True
        subtree[src] = 1
        self.cur_size += 1
        for adj in self.tree[src]:
            if not visited[adj] and not self.iscentroid[adj]:
                self.dfs(adj, visited, subtree)
                subtree[src] += subtree[adj]
    
    def findCentroid(self, src, visited, subtree):
        iscentroid = True
        visited[src] = True
        heavy_node = 0
        for adj in self.tree[src]:
            if not visited[adj] and not self.iscentroid[adj]:
                if subtree[adj] >  self.cur_size//2:
                    iscentroid = False
                
                if heavy_node == 0 or subtree[adj] > subtree[heavy_node]:
                    heavy_node = adj
            
        if iscentroid and self.cur_size - subtree[src] <= self.cur_size//2:
            return src
        else:
            return self.findCentroid(heavy_node, visited, subtree)

    def findCentroidUtil(self, src):
        visited = [False] * self.size
        subtree = [0] * self.size
        self.cur_size = 0
        self.dfs(src, visited, subtree)
        for i in range(self.size):
            visited[i] = False
        centroid = self.findCentroid(src, visited, subtree)
        self.iscentroid[centroid] = True
        return centroid

    def decomposeTree(self, root,ch):
        centroid_tree = self.findCentroidUtil(root)
        self.characters[centroid_tree]=ch
        for adj in self.tree[centroid_tree]:
            if not self.iscentroid[adj]:
                centroid_subtree = self.decomposeTree(adj,ch+1)
                self.ctree[centroid_tree].append(centroid_subtree)
                self.ctree[centroid_subtree].append(centroid_tree)
            
        return centroid_tree

    def addEdge(self, src, dest):
        self.tree[src].append(dest)
        self.tree[dest].append(src)

    def printf(self,n):
        newlist=[]
        for i in range(1,len(self.characters)):
            newlist.append(self.characters[i])
        return newlist


    

if __name__ == '__main__':
    n=int(sys.stdin.readline())
    tree = Tree(n)
    for _ in range(n-1):
        a,b=map(int,sys.stdin.readline().split())
        tree.addEdge(a, b)
        
    tree.decomposeTree(1,65)
    centroidtree=tree.printf(4)
    for i in  centroidtree:
        sys.stdout.write(str(chr(i)) +" ")
    
