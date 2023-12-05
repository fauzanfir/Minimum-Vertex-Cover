import argparse
import tracemalloc
import networkx as nx
import operator
import time
import os

def addEdge(adj, x, y):
	adj[x].append(y)
	adj[y].append(x)


def dfs(adj, dp, src, par):
	for child in adj[src]:
		if child != par:
			dfs(adj, dp, child, src)

	for child in adj[src]:
		if child != par:
			dp[src][0] = dp[child][1] + dp[src][0]
			dp[src][1] = dp[src][1] + min(dp[child][1], dp[child][0])


def minSizeVertexCover(adj, N):
	dp = [[0 for j in range(2)] for i in range(N+1)]
	for i in range(1, N+1):
		dp[i][0] = 0
		dp[i][1] = 1

	dfs(adj, dp, 1, -1)

	print(min(dp[1][0], dp[1][1]))

def readTreeFromFile(filename):
	with open(filename, 'r') as file:
		lines = file.readlines()
		N = int(lines[0])
		adj = [[] for _ in range(N+1)]
		for i in range(1, len(lines[1:])+1):
			adj[i] = list(map(int, lines[i].split()))
		return adj, N

def create_graph(adj_list):
	G = nx.Graph()
	for i in range(len(adj_list)):
		for j in adj_list[i]:
			G.add_edge(i + 1, j)
	return G

def BnB(G, T):
	start_time=time.time()
	end_time=start_time
	delta_time=end_time-start_time
	times=[]   

	OptVC = []
	CurVC = []
	Frontier = []
	neighbor = []

	UpperBound = G.number_of_nodes()
	print('Initial UpperBound:', UpperBound)

	CurG = G.copy() 
	v = find_maxdeg(CurG)
	Frontier.append((v[0], 0, (-1, -1)))  
	Frontier.append((v[0], 1, (-1, -1)))

	while Frontier!=[] and delta_time<T:
		(vi,state,parent)=Frontier.pop() 
		backtrack = False

		if state == 0:  
			neighbor = CurG.neighbors(vi) 
			for node in list(neighbor):
				CurVC.append((node, 1))
				CurG.remove_node(node) 
		elif state == 1:  
			CurG.remove_node(vi)  
		else:
			pass

		CurVC.append((vi, state))
		CurVC_size = VC_Size(CurVC)

		if CurG.number_of_edges() == 0: 
			if CurVC_size < UpperBound:
				OptVC = CurVC.copy()
				print('Current Opt VC size', CurVC_size)
				UpperBound = CurVC_size
				times.append((CurVC_size,time.time()-start_time))
			backtrack = True
				
		else:  
			CurLB = Lowerbound(CurG) + CurVC_size

			if CurLB < UpperBound:  
				vj = find_maxdeg(CurG)
				Frontier.append((vj[0], 0, (vi, state)))
				Frontier.append((vj[0], 1, (vi, state)))

			else:
				backtrack=True

		if backtrack==True:
			if Frontier != []:	
				nextnode_parent = Frontier[-1][2]	

				if nextnode_parent in CurVC:
					
					id = CurVC.index(nextnode_parent) + 1
					while id < len(CurVC):	
						mynode, mystate = CurVC.pop()	
						CurG.add_node(mynode)	
						
						
						curVC_nodes = list(map(lambda t:t[0], CurVC))
						for nd in G.neighbors(mynode):
							if (nd in CurG.nodes()) and (nd not in curVC_nodes):
								CurG.add_edge(nd, mynode)	

				elif nextnode_parent == (-1, -1):
					CurVC.clear()
					CurG = G.copy()
				else:
					print('error in backtracking step')

		end_time=time.time()
		delta_time=end_time-start_time
		if delta_time>T:
			print('Cutoff time reached')

	return OptVC,times

def find_maxdeg(g):
	deglist = dict(g.degree())
	deglist_sorted = sorted(deglist.items(), reverse=True, key=operator.itemgetter(1))  # sort in descending order of node degree
	v = deglist_sorted[0]  # tuple - (node,degree)
	return v

def Lowerbound(graph):
	lb=graph.number_of_edges() / find_maxdeg(graph)[1]
	lb=ceil(lb)
	return lb


def ceil(d):
    if d > int(d):
        return int(d) + 1
    else:
        return int(d)
    
def VC_Size(VC):
	vc_size = 0
	for element in VC:
		vc_size = vc_size + element[1]
	return vc_size

N = [10000, 100000, 1000000]
bnb_n = [45, 100, 135]
for i in range(len(N)):
	adj, n = readTreeFromFile("data_" + str(N[i]) +"_vertex.txt")
	start = time.time()
	tracemalloc.start()
	minSizeVertexCover(adj, n)
	end = time.time()
	mem1 = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	print(mem1[1])
	print(str(end - start))
	

	for j in range(1, bnb_n[i] + 1):
		adj[j] = [ele for ele in adj[j] if ele <= bnb_n[i]]

	g = create_graph(adj[1:bnb_n[i]+1])
	print('No of nodes in G:', g.number_of_nodes(),
		  '\nNo of Edges in G:', g.number_of_edges())
	
	start = time.time()
	tracemalloc.start()
	Sol_VC,times = BnB(g, 10000)

	for element in Sol_VC:
		if element[1]==0:
			Sol_VC.remove(element)
	end = time.time()
	mem2 = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	print(mem2[1])
	print(str(end - start))