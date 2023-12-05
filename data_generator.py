import random

def addEdge(adj, x, y):
	adj[x].append(y)
	adj[y].append(x)
	
def writeTreeToFile(adj, filename):
    with open(filename, "w") as file:
        file.write(f"{len(adj) - 1}\n")
        for edge in adj[1:]:
            file.write(" ".join(map(str, edge)) + "\n")

def generate_tree(n):
    adj = [[] for _ in range(n + 1)]

    for i in range(2, n + 1):
        parent = random.randint(1, i - 1)
        addEdge(adj, parent, i)

    return adj


N = [1000, 100000, 1000000]
for n in N:
    adj = generate_tree(n)
    writeTreeToFile(adj, "data_" + str(n) +"_vertex.txt")
