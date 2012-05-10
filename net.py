import sys, os
sys.path.append('/'.join(os.path.os.path.abspath(__file__).split('/')[:-1]) + '/lib')
import networkx as nx
import bisect, time, random, Gnuplot, numpy

font = "Helvetica,20"
fname = 'pics/dijkstra.ps'

def dijkstra(howmany):
    G = nx.fast_gnp_random_graph(howmany, 0.5)
    #print 'graph generated'
    nodes = G.nodes()

    rands1 = list(numpy.random.randint(len(nodes)-1, size = 1000))
    rands2 = list(numpy.random.randint(len(nodes)-1, size = 1000))

    for i in range(len(rands1)):
        while rands1[i] == rands2[i]:
            rands2[i] = random.randint(0, len(nodes)-1)

    start = time.time()
    for s, e in zip(rands1, rands2):
        #print '%d %d %d' % (s, e, len(nodes))
        nx.dijkstra_path(G, nodes[s], nodes[e])
    t = time.time() - start

    return t

def main():
    tulos_lista = []
    g = Gnuplot.Gnuplot()
    
    g('set title "Polkujen laskeminen Dijkstran algoritmilla" font "%s"' % font)
    g('set xlabel "Soluja graafissa" font "%s"' % font)
    g('set ylabel "Kulunut aika [s]" font "%s"' % font)
    g('set style data linespoints')

    for i in range(1, 6):
        howmany = 200*i
        t = dijkstra(howmany)
        tulos_lista.append((howmany, t))
        print '%d\t%.2f' % (howmany, t)

    g.plot(tulos_lista)
    input = raw_input('Paina y tallentaaksesi...\n')
    if input == 'y':
        g.hardcopy(fname, color=1)
    

if __name__ == '__main__':
	main()
