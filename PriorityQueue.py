import Queue, time, random, Gnuplot, heapq, numpy

# Huom: Oneiricissa tama vaatii python-gnuplot ja gtk2-engines-pixbuf paketit

# Dokumentointia:
# http://docs.python.org/library/queue.html#Queue.PriorityQueue

font = "Helvetica,20"

lisays_testi = False
lmax_koko = 1000000 # Jonon koko. Nollalla jonolle ei aseteta maksimikokoa
ltesti_koko = 1000000 # Kuinka monella alkiolla testataan
lmin_num = 0 # Minimiarvo alkiolle
lmax_num = 100000 # Maksimiarvo alkiolle
lheapq_testi = True # Testaa heapq kirjastoa, muuten Queue-kirjaston prority queue
lmittauspisteita = 10
if lheapq_testi == True:
	pqadd_fname = "pics/pr_heapq_add.ps"
else:
	pqadd_fname = "pics/pr_queue_add.ps"

merge_testi = False
merge_toinen_lista_vakio_kokoinen = False
mmax_koko = 10000000 # Jonon koko. Nollalla jonolle ei aseteta maksimikokoa
mtesti_koko = 10000000 # Kuinka monella alkiolla testataan
mmin_num = 0 # Minimiarvo alkiolle
mmax_num = 100000 # Maksimiarvo alkiolle
mheapq_testi = True # Testaa heapq kirjastoa, muuten Queue-kirjaston prority queue
mmittauspisteita = 10
if mheapq_testi == True and merge_toinen_lista_vakio_kokoinen == True:
	pqmerge_fname = "pics/pr_queue_merge_diff_size.ps"
elif mheapq_testi == True and merge_toinen_lista_vakio_kokoinen == False:
	pqmerge_fname = "pics/pr_queue_merge_same_size.ps"
elif mheapq_testi == False and merge_toinen_lista_vakio_kokoinen == True:
	pqmerge_fname = "pics/pr_heapq_merge_diff_size.ps"
elif mheapq_testi == False and merge_toinen_lista_vakio_kokoinen == False:
	pqmerge_fname = "pics/pr_heapq_merge_same_size.ps"

poisto_testi = True
pmax_koko = 1000000 # Jonon koko. Nollalla jonolle ei aseteta maksimikokoa
ptesti_koko = 1000000 # Kuinka monella alkiolla testataan
pmin_num = 0 # Minimiarvo alkiolle
pmax_num = 100000 # Maksimiarvo alkiolle
pheapq_testi = False # Testaa heapq kirjastoa, muuten Queue-kirjaston prority queue
pmittauspisteita = 10
if lheapq_testi == True:
	pqdel_fname = "pics/pr_heapq_del.ps"
else:
	pqdel_fname = "pics/pr_queue_del.ps"

# Testaa kaikenlaisia jono-operaatioita.
# Param heap_queue: Testaa heapq kirjastoa, muuten Queue-kirjaston prority queue
def queue_lisays(pr_jono, montako, mittausvali, heap_queue, rands):
	ret = [] # Tulokset (indeksi, arvo) tupleina
	print 'Lisataan %d satunnaista int alkiota' % len(rands)
	aloitusaika = time.time()
	if heap_queue == True:
		i = 0
		for rand in rands:
			heapq.heappush(pr_jono, rand)
			if (i+1) % mittausvali == 0:
				ret.append((i, time.time() - aloitusaika))
			i += 1
	else:
		i = 0
		for rand in rands:
			pr_jono.put(rand)
			if (i+1) % mittausvali == 0:
				ret.append((i, time.time() - aloitusaika))
			i += 1
	lopetusaika = time.time()
	kulunut_aika = lopetusaika - aloitusaika
	print 'Valmis. Aikaa kului %.2f sekuntia' % kulunut_aika
	return ret

# Testaa lisays-jono-operaation.
# Param heap_queue: Testaa heapq kirjastoa, muuten Queue-kirjaston prority queue
def queue_lisays_testi(heap_queue):
	
	g = Gnuplot.Gnuplot()
	if heap_queue == True:
		g('set title "Prioriteettijono: Satunnaisten alkioiden lisays heapq kirjastolla" font "%s"' % font)
		pr_jono = []
	else:
		g('set title "Prioriteettijono: Satunnaisten alkioiden lisays Queue kirjastolla" font "%s"' % font)
		pr_jono = Queue.PriorityQueue(maxsize = lmax_koko)
	rands = list(numpy.random.randint(lmax_num, size = ltesti_koko))
	tulos_lista = []
	g('set xlabel "Lisattyja alkioita" font "%s"' % font)
	g('set ylabel "Kulunut aika [s]" font "%s"' % font)
	g('set style data linespoints')

	tulos_lista = queue_lisays(pr_jono = pr_jono, montako = ltesti_koko, \
		mittausvali = ltesti_koko/lmittauspisteita, heap_queue = heap_queue, rands = rands)
	
	g.plot(tulos_lista)
	input = raw_input('Paina y tallentaaksesi...\n')
	if input == 'y':
		g.hardcopy(pqadd_fname, color=1)

def queue_merge_testi(toinen_vakio_koko):
	tuloslista = []
	g = Gnuplot.Gnuplot()
	if toinen_vakio_koko == True:
		g('set title "Prioriteettijono: Eripituisten prioriteettijonojen yhdistely heapq kirjastolla" font "%s"' % font)
		g('set xlabel "Alkioita lyhyemmassa listassa" font "%s"' % font)
	else:
		g('set title "Prioriteettijono: Saman pituisten prioriteettijonojen yhdistely heapq kirjastolla" font "%s"' % font)
		g('set xlabel "Alkioita listoissa" font "%s"' % font)
	g('set ylabel "Kulunut aika [s]" font "%s"' % font)
	g('set style data linespoints')

	mittausvali = mtesti_koko / mmittauspisteita

	pr_jono_eka = list(numpy.random.randint(mmax_num, size = mtesti_koko))
	pr_jono_toka = list(numpy.random.randint(mmax_num, size = mtesti_koko))

	for i in range(mtesti_koko):
		alkioita = i+1
		if alkioita % mittausvali == 0:
			
			pr_jono_eka_cp = pr_jono_eka[:alkioita]
			if toinen_vakio_koko == True:
				pr_jono_toka_cp = pr_jono_toka[:]
			else:
				pr_jono_toka_cp = pr_jono_toka[:alkioita]
			heapq.heapify(pr_jono_eka_cp)
			heapq.heapify(pr_jono_toka_cp)
			
			aloitusaika = time.time()
			yhdistetty = heapq.merge(pr_jono_eka_cp, pr_jono_toka_cp)
			lopetusaika = time.time()
			kulunut_aika = lopetusaika - aloitusaika
			tuloslista.append((alkioita, kulunut_aika))
			#print 'Valmis. Alkioita %d, aikaa kului %.6f sekuntia' % \
			#	(len(pr_jono_eka_cp), kulunut_aika)

	g.plot(tuloslista)
	input = raw_input('Paina y tallentaaksesi...\n')
	if input == 'y':
		g.hardcopy(pqmerge_fname, color=1)

def queue_poisto_testi(heapq_testi):
	tuloslista = []
	g = Gnuplot.Gnuplot()
	g('set xlabel "Alkioita poistettu" font "%s"' % font)
	g('set ylabel "Kulunut aika [s]" font "%s"' % font)
	g('set style data linespoints')

	mittausvali = ptesti_koko / pmittauspisteita

	if heapq_testi == False:
		g('set title "Prioriteettijonon poistotesti Queue kirjastolla" font "%s"' % font)
		pr_jono = Queue.PriorityQueue(maxsize = pmax_koko)
		for i in range(ptesti_koko):
			pr_jono.put(numpy.random.randint(pmax_num))
	else:
		g('set title "Prioriteettijonon poistotesti heapq kirjastolla" font "%s"' % font)
		pr_jono = list(numpy.random.randint(pmax_num, size = ptesti_koko))
		heapq.heapify(pr_jono)

	aloitusaika = time.time()
	if heapq_testi == False:
		for i in range(ptesti_koko):
			pr_jono.get()
			if (i+1) % mittausvali == 0:
				valiaika = time.time()
				kulunut_aika = valiaika - aloitusaika
				tuloslista.append((i+1, kulunut_aika))
	else:
		for i in range(ptesti_koko):
			heapq.heappop(pr_jono)
			if (i+1) % mittausvali == 0:
				valiaika = time.time()
				kulunut_aika = valiaika - aloitusaika
				tuloslista.append((i+1, kulunut_aika))


	g.plot(tuloslista)
	input = raw_input('Paina y tallentaaksesi...\n')
	if input == 'y':
		g.hardcopy(pqdel_fname, color=1)

def main():
	print 'testing'
	if lisays_testi:
		queue_lisays_testi(lheapq_testi)
	if merge_testi:
		queue_merge_testi(merge_toinen_lista_vakio_kokoinen)
	if poisto_testi:
		queue_poisto_testi(pheapq_testi)




main()

