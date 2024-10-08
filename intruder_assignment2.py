# This version: September 27th, 2022
# Programmer: Ludolf Meester, Etienne Guichard
import matplotlib.pyplot as plt
import numpy as np

# Reading data and setup list of edges
filename = 'airport-graph.txt'
# Conventions the input file must satisfy:
#     two integers per line, denoting two nodes connected by an edge
#     source node has number 0; highest number is the terminal node
with open(filename) as file_object:
    lines = file_object.readlines()

edges = np.array([tuple(map(int, line.split())) for line in lines])
nedges = len(edges)
print("List of", nedges, "edges read from", filename, ":")
print(edges)
# determine t(erminal)node
tnode = 0
tnode = max([max(e) for e in edges])
print("Terminal node:", tnode)


# Function sysfail
def sysfail(failed, tnode, maxpathlen):
    # input:
    #    failed: a list of tuples (n1,n2), representing the failed edges
    #    tnode: terminal node number
    #    maxpathlen: length of longest path from 0 to tnode
    breach = 0
    # construct the incidence matrix:
    Imat = np.zeros((tnode + 1, tnode + 1), dtype='int')
    failedarr = np.array(failed)
    if failedarr.shape[0] != 0:
        Imat[failedarr[:, 0], failedarr[:, 1]] = Imat[failedarr[::-1, 1], failedarr[::-1, 0]] = 1
    # if node 0 or tnode is isolated a breach is impossible
    if np.min([np.max(Imat[0, :]), np.max(Imat[:, tnode])]) == 0:
        return breach
    A = Imat
    #  if i-th power of Imat has nonzero (0,tnode) element, there is a
    # path of length i from 0 -> tnode: a breach
    for i in range(1, maxpathlen):
        if A[0, tnode] > 0:
            breach = 1
            break
        A = np.matmul(A, Imat)
    return breach


# Simulation
seedval = 3875663
np.random.seed(seedval)
ntot = 1000
q = 0.2
maxpathlen = 20
breaches = 0

ks = np.array([5, 8, 11, 14, 17])
nvals = np.round(1 / ks**2 / sum(1/ks**2) * 1000)

while sum(nvals) > 1000:
    nvals[0] = nvals[0] - 1
while sum(nvals) < 1000:
    nvals[0] = nvals[0] + 1

nvals = np.array(nvals, dtype=int)
print('sum of samples: {}'.format(sum(nvals)))
prob_arr = []
for nrep, k in zip(nvals, ks):
    print('running nk = {} repetitions for k={}'.format(nrep, k))
    for i in range(nrep):
        # create list of failed edges:
        failed = edges[np.random.choice(22, size=k)]
        breaches += sysfail(failed, tnode, maxpathlen)
    print('detected {} security breaches, probability estimate P(B|Y={}) = {}'.format(breaches, k, breaches/nrep))
    prob_arr.append(breaches/nrep)
    breaches = 0

prob_arr = np.array(prob_arr)

prob_all = np.empty(len(edges), dtype=float)
ks_all = np.arange(0, len(edges), 1)

prob_all[0:4] = 0.0 # k<4 -> prob is zero
prob_all[19:] = 1.0 # k > 19 -> prob is one
prob_all[ks-1] = prob_arr

where_interp = [k for k in np.arange(4, 19, 1) if k not in ks-1]
where_known = [k for k in ks_all if k not in where_interp]

prob_interpolated = np.interp(ks_all[where_interp], ks_all[where_known], prob_all[where_known], left=0, right=1)
prob_all[where_interp] = prob_interpolated

qs = [1e-3, 2e-3, 5e-3, 7e-3, 1e-2, 2e-2, 5e-2, 7e-2, 0.1, 0.2]
pbs = [0.0]*len(qs)
N = len(edges)
for index, q in enumerate(qs):
    for k in ks_all:
        p_y_eq_k = q**k * (1-q)**(N - k)
        p_b_given_y = prob_all[k-1]
        pbs[index] += p_b_given_y*p_y_eq_k

print(qs, pbs)


plt.style.use('ggplot')
fig, ax = plt.subplots()

for k in ks:
    ax.axvline(k, color='k', linestyle='dashed')
for k in [3, 20]:
    ax.axvline(k, color='b', linestyle='dashed')

ax.plot(ks_all+1, prob_all)
ax.set_xlabel('$k$')
ax.set_ylabel('$P(B|Y=k)$')
ax.set_xlim(0, len(edges))
plt.show()
plt.clf()
plt.close()

fig, ax = plt.subplots()

ax.plot(qs, pbs)
ax.set_xlabel('$q$')
ax.set_ylabel('$P(B)$')
ax.set_xscale('log')
plt.show()

