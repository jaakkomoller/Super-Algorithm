import bisect, time, random, Gnuplot, numpy

# Huom: Oneiricissa tama vaatii python-gnuplot ja gtk2-engines-pixbuf paketit


font = "Helvetica,20"

lisays_testi = True
ltesti_koko = 100000 # Kuinka monella alkiolla testataan
lmin_num = 0 # Minimiarvo alkiolle
lmax_num = 100000 # Maksimiarvo alkiolle
lmittauspisteita = 30
badd_fname = 'pics/binary_add.ps'

etsi_testi = False
#testi_koko = 10000000 # Kuinka monella alkiolla testataan
#min_num = 0 # Minimiarvo alkiolle
#max_num = 100000 # Maksimiarvo alkiolle
#mittauspisteita = 30
#etsittavia = 10000
#bsearch_fname = 'pics/binary_search.ps'

def index(a, x):
	'Locate the leftmost value exactly equal to x'
	i = bisect.bisect_left(a, x)
	if i != len(a) and a[i] == x:
		return i
	raise ValueError

# Testaa kaikenlaisia jono-operaatioita.
def queue_lisays(bi_jono, mittausvali, rands):
	ret = [] # Tulokset (indeksi, arvo) tupleina
	print 'Lisataan %d satunnaista int alkiota' % len(rands)
	aloitusaika = time.time()
	i = 0
	for rand in rands:
		bisect.insort(bi_jono, rand)
		if (i+1) % mittausvali == 0:
			ret.append((i, time.time() - aloitusaika))
		i += 1
	lopetusaika = time.time()
	kulunut_aika = lopetusaika - aloitusaika
	print 'Valmis. Aikaa kului %.2f sekuntia' % kulunut_aika
	return ret

# Testaa lisays-jono-operaation.
def queue_lisays_testi():
	
	g = Gnuplot.Gnuplot()
	bi_jono = []
	
	rands = list(numpy.random.randint(lmax_num, size = ltesti_koko))
	
	tulos_lista = []
	g('set title "Satunnaisten alkioiden lisays binaarijono kirjastolla" font "%s"' % font)
	g('set xlabel "Lisattyja alkioita" font "%s"' % font)
	g('set ylabel "Kulunut aika [s]" font "%s"' % font)
	g('set style data linespoints')

	tulos_lista = queue_lisays(bi_jono = bi_jono, \
		mittausvali = ltesti_koko/lmittauspisteita, rands = rands)
	
	g.plot(tulos_lista)
	input = raw_input('Paina y tallentaaksesi...\n')
	if input == 'y':
		g.hardcopy(badd_fname, color=1)

# Etsii annetun avaimen binaarijonosta
# Palauttaa etsimiseen kuluneen ajan
def queue_etsi_avain_testi(bjono, avain):
	aaika = time.time()
	index(bjono, avain)
	laika = time.time()
	return laika - aaika

def etsi_testi():

# OK arvot:
# testi_koko = 10000000 # Kuinka monella alkiolla testataan
# max_num = 100000 # Maksimiarvo alkiolle
# etsittavia = 2000

	g = Gnuplot.Gnuplot()
	bjono = []
	tulos_lista = []

#	g.xlabel('Alkioita taulussa')
	g.__call__('set title "Etsimiseen kuluva aika binaarijonokirjastolla" font "%s"' % font)
	g.__call__('set xlabel "Alkioita taulussa" font "%s"' % font)
	g.__call__('set ylabel "%d hakuun kulunut aika [s]" font "%s"' % (etsittavia, font))
	g('set style data linespoints')
	
	rands = list(numpy.random.randint(max_num, size = testi_koko))
	mittausvali = testi_koko/mittauspisteita

	for rand in rands:
#		bisect.insort(bjono, rand)
		bjono.append(rand)
		if (len(bjono)) % mittausvali == 0:
			bjono.sort()
			aika = 0
			for a in range(etsittavia):
				etsittava = rands[numpy.random.randint(len(bjono)-1)]
				aika += queue_etsi_avain_testi(bjono, etsittava)
			tulos_lista.append((len(bjono), aika))

	g.plot(tulos_lista)
	input = raw_input('Paina y tallentaaksesi...\n')
	if input == 'y':
		g.hardcopy(bsearch_fname, color=1)

def main():
	print 'testing'
	if lisays_testi == True:
		queue_lisays_testi()
	if etsi_testi == True:
		etsi_testi()

main()
