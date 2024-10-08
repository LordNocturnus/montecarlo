# This version: September 27th, 2022
# Programmer: Ludolf Meester, Etienne Guichard

import numpy as np

# Reading data and setup list of edges
filename = 'airport-graph.txt'
# Conventions the input file must satisfy:
#     two integers per line, denoting two nodes connected by an edge
#     source node has number 0; highest number is the terminal node
with open(filename) as file_object:
    lines = file_object.readlines()
edges = [tuple(map(int, line.split())) for line in lines] 
nedges = len(edges)
print("List of", nedges, "edges read from", filename, ":")
print(edges)
# determine t(erminal)node
tnode = 0
tnode = max(max(edges))
print("Terminal node:",tnode)

# Function sysfail
def sysfail(failed, tnode, maxpathlen):
    # input:
    #    failed: a list of tuples (n1,n2), representing the failed edges
    #    tnode: terminal node number
    #    maxpathlen: length of longest path from 0 to tnode
    breach = 0
    # construct the incidence matrix:
    Imat = np.zeros((tnode+1,tnode+1),dtype='int')
    failedarr = np.array(failed)
    if failedarr.shape[0] != 0:
        Imat[failedarr[:,0],failedarr[:,1]] = Imat[failedarr[::-1,1],failedarr[::-1,0]]= 1
    # if node 0 or tnode is isolated a breach is impossible
    if np.min([np.max(Imat[0,:]),np.max(Imat[:,tnode])]) == 0:
        return breach
    A = Imat
    #  if i-th power of Imat has nonzero (0,tnode) element, there is a
    # path of length i from 0 -> tnode: a breach
    for i in range(1,maxpathlen):
        if A[0,tnode]>0:
            breach = 1
            break
        A = np.matmul(A,Imat)
    return breach

# Simulation
seedval = 3875663
np.random.seed(seedval)
nrep = 1000
q = 0.2
maxpathlen = 10
breaches = 0

print("Simulating", nrep, "replications for q=", q, "and seedvalue", seedval)
for i in range(nrep):
    unif = np.random.random(nedges)
    # create list of failed edges:
    failed = [edge for ind,edge in enumerate(edges) if unif[ind] < q]
    breaches += sysfail(failed, tnode, maxpathlen)
        
print("There were", breaches, "security breaches. Estimated P(breach)=",breaches/nrep)

