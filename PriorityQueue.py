import Queue, time, random, Gnuplot, heapq, numpy

# Huom: Oneiricissa tama vaatii python-gnuplot ja gtk2-engines-pixbuf paketit

# Dokumentointia:
# http://docs.python.org/library/queue.html#Queue.PriorityQueue

max_koko = 10000000 # Jonon koko. Nollalla jonolle ei aseteta maksimikokoa
testi_koko = 10000000 # Kuinka monella alkiolla testataan
min_num = 0 # Minimiarvo alkiolle
max_num = 100000 # Maksimiarvo alkiolle
heapq_testi = False # Testaa heapq kirjastoa, muuten Queue-kirjaston prority queue
mittauspisteita = 10

lisays_testi = False
merge_testi = False
merge_toinen_lista_vakio_kokoinen = True
poisto_testi = True

# Testaa kaikenlaisia jono-operaatioita.
# Param heap_queue: Testaa heapq kirjastoa, muuten Queue-kirjaston prority queue
def queue_lisays(pr_jono, montako, mittausvali, heap_queue):
	ret = [] # Tulokset (indeksi, arvo) tupleina
	print 'Lisataan %d satunnaista int alkiota' % montako
	aloitusaika = time.time()
	if heap_queue == True:
		for i in range(montako):
			heapq.heappush(pr_jono, random.randint(min_num, max_num))
			if (i+1) % mittausvali == 0:
				ret.append((i, time.time() - aloitusaika))
	else:
		for i in range(montako):
			pr_jono.put(random.randint(min_num, max_num))
			if (i+1) % mittausvali == 0:
				ret.append((i, time.time() - aloitusaika))
	lopetusaika = time.time()
	kulunut_aika = lopetusaika - aloitusaika
	print 'Valmis. Aikaa kului %.2f sekuntia' % kulunut_aika
	return ret

# Testaa lisays-jono-operaation.
# Param heap_queue: Testaa heapq kirjastoa, muuten Queue-kirjaston prority queue
def queue_lisays_testi(heap_queue):
	
	g = Gnuplot.Gnuplot()
	if heap_queue == True:
		g.title('Satunnaisten alkioiden lisays heapq kirjastolla')
		pr_jono = []
	else:
		g.title('Satunnaisten alkioiden lisays Queue kirjastolla')
		pr_jono = Queue.PriorityQueue(maxsize = max_koko)
	tulos_lista = []
	g.xlabel('Lisattyja alkioita')
	g.ylabel('Kulunut aika')
	g('set style data linespoints')

	tulos_lista = queue_lisays(pr_jono = pr_jono, montako = testi_koko, \
		mittausvali = testi_koko/mittauspisteita, heap_queue = heap_queue)
	
	g.plot(tulos_lista)
	raw_input('Paina jotain jatkaaksesi...\n')

def queue_merge_testi(toinen_vakio_koko):
	tuloslista = []
	g = Gnuplot.Gnuplot()
	if toinen_vakio_koko == True:
		g.title('Eripituisten prioriteettijonojen yhdistely heapq kirjastolla')
		g.xlabel('Alkioita lyhyemmassa listassa')
	else:
		g.title('Saman pituisten prioriteettijonojen yhdistely heapq kirjastolla')
		g.xlabel('Alkioita listoissa')
	g.ylabel('Kulunut aika')
	g('set style data linespoints')

	mittausvali = testi_koko / mittauspisteita

	pr_jono_eka = list(numpy.random.randint(max_num, size = testi_koko))
	pr_jono_toka = list(numpy.random.randint(max_num, size = testi_koko))

	for i in range(testi_koko):
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
	raw_input('Paina jotain jatkaaksesi...\n')

def queue_poisto_testi(heapq_testi):
	tuloslista = []
	g = Gnuplot.Gnuplot()
	g.xlabel('Alkioita poistettu')
	g.ylabel('Kulunut aika')
	g('set style data linespoints')

	mittausvali = testi_koko / mittauspisteita

	if heapq_testi == False:
		g.title('Prioriteettijonon poistotesti Queue kirjastolla')
		pr_jono = Queue.PriorityQueue(maxsize = max_koko)
		for i in range(testi_koko):
			pr_jono.put(numpy.random.randint(max_num))
	else:
		g.title('Prioriteettijonon poistotesti heapq kirjastolla')
		pr_jono = list(numpy.random.randint(max_num, size = testi_koko))
		heapq.heapify(pr_jono)

	mittausvali = testi_koko / mittauspisteita

	aloitusaika = time.time()
	if heapq_testi == False:
		for i in range(testi_koko):
			pr_jono.get()
			if (i+1) % mittausvali == 0:
				valiaika = time.time()
				kulunut_aika = valiaika - aloitusaika
				tuloslista.append((i+1, kulunut_aika))
	else:
		for i in range(testi_koko):
			heapq.heappop(pr_jono)
			if (i+1) % mittausvali == 0:
				valiaika = time.time()
				kulunut_aika = valiaika - aloitusaika
				tuloslista.append((i+1, kulunut_aika))


	g.plot(tuloslista)
	raw_input('Paina jotain jatkaaksesi...\n')

def main():
	print 'testing'
	if lisays_testi:
		queue_lisays_testi(heapq_testi)
	if merge_testi:
		queue_merge_testi(merge_toinen_lista_vakio_kokoinen)
	if poisto_testi:
		queue_poisto_testi(heapq_testi)




main()

