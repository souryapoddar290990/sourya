import sys,time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import matshow, show, cm
from optparse import OptionParser

def normalize(A):
    column_sums = A.sum(axis=0)
    return A / column_sums[np.newaxis, :]

def inflate(A, inflate_factor): return normalize(np.power(A, inflate_factor))

def expand(A, expand_factor): return np.linalg.matrix_power(A, expand_factor)

def add_diag(A, mult_factor): return A + mult_factor * np.identity(A.shape[0])

def get_clusters(A):
    clusters,clust_map = [],{}
    for i, r in enumerate((A>0).tolist()):
        if r[i]: clusters.append(A[i,:]>0)
    for cn , c in enumerate(clusters):
        for x in  [ i for i, x in enumerate(c) if x ]: clust_map[cn] = clust_map.get(cn, [])  + [x]
    return clust_map

def draw(G, A, cluster_map):
    clust_map,colors = {},[]
    for k, vals in cluster_map.items():
        for v in vals: clust_map[v] = k
    for i in range(len(G.nodes())): colors.append(clust_map.get(i, 100))
    pos = nx.spring_layout(G)
    plt.figure(2)
    nx.draw_networkx_nodes(G, pos,node_size = 200, node_color =colors , cmap=plt.cm.Blues )
    nx.draw_networkx_edges(G,pos, alpha=0.5)
    matshow(A, fignum=1, cmap=cm.gray)
    plt.show()
    show()

def stop(M, i):
    if i%5 == 4:
        m = np.max( M**2 - M) - np.min( M**2 - M)
        if m == 0: return True            
    return False

def mcl(M, expand_factor = 2, inflate_factor = 2, max_loop = 10 , mult_factor = 1):
    M = add_diag(M, mult_factor)
    M = normalize(M)
    for i in range(max_loop):
        M = inflate(M, inflate_factor)
        M = expand(M, expand_factor)
        if stop(M, i): break
    return M, get_clusters(M)

def networkx_mcl(G, expand_factor = 2, inflate_factor = 2, max_loop = 10 , mult_factor = 1):
    A = nx.adjacency_matrix(G)
    return mcl(np.array(A.todense()), expand_factor, inflate_factor, max_loop, mult_factor)

def print_info(options): print("-" * 60+"\nMARKOV CLUSTERING:\n"+"-" * 60+"\nexpand_factor: "+str(options.expand_factor)+"\ninflate_factor: "+str(options.inflate_factor)+"\nmult factor: "+str(options.mult_factor)+"\nmax loops: "+str(options.max_loop))+"\n"

def get_options():
    usage = "usage: %prog [options] <input_matrix>"
    parser = OptionParser(usage)
    parser.add_option("-e", "--expand_factor",dest="expand_factor",default=2,type=int,help="expand factor (default: %default)")
    parser.add_option("-i", "--inflate_factor",dest="inflate_factor",default=2,type=float,help="inflate factor (default: %default)")
    parser.add_option("-m", "--mult_factor",dest="mult_factor",default=2,type=float,help="multiply factor (default: %default)")
    parser.add_option("-l", "--max_loops",dest="max_loop",default=60,type=int,help="max loops (default: %default)")
    parser.add_option("-o", "--output", metavar="FILE", help="output (default: stdout)")
    parser.add_option("-v", "--verbose",action="store_true", dest="verbose", default=True,help="verbose (default: %default)")
    parser.add_option("-d", "--draw-graph",action="store_true", dest="draw", default=False,help="show graph with networkx (default: %default)")
    (options, args) = parser.parse_args()
    try: filename = args[0]
    except: raise Exception('input', 'missing input filename')
    return options, filename

def get_graph(csv_filename):
    M = []
    for r in open(csv_filename):
        r = r.strip().split(",")
        M.append(list(map(lambda x: float(x.strip()), r)))
    return np.array(M), nx.from_numpy_matrix(np.matrix(M))

def clusters_to_output(clusters, options):
    if options.output and len(options.output)>0:
        f = open(options.output, 'w')
        for k, v in clusters.items(): f.write("%s|%s\n" % (k, ", ".join(map(str, v)) ))
        f.close()
    else:
        print("Clusters:")
        for k, v in clusters.items(): print('{}, {}'.format(k, v))

if __name__ == '__main__':
    options, filename = get_options()
    print_info(options)
    M, G = get_graph(filename)
    # print("number of nodes: %s\n" % M.shape[0])
    # print(str(time.time())+" evaluating clusters...")
    M, clusters = networkx_mcl(G, expand_factor = options.expand_factor,inflate_factor = options.inflate_factor,max_loop = options.max_loop,mult_factor = options.mult_factor)
    print(str(time.time())+"done\n")
    clusters_to_output(clusters, options)
    if options.draw:
        # print(str(time.time())+": drawing...")
        draw(G, M, clusters)
        # print(str(time.time())+": done")