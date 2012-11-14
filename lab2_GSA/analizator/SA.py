import sys

class Stog:
  
  def __init__(self):
    self.stog = []


  def push (self, e):
    self.stog.append(e)

  def pop (self):
    if self.prazan():
      return False
    return self.stog.pop()

  def vrh (self):
    if self.prazan():
      return False
    
    return self.stog[-1]

  def dohvati (self, n):  
    if n > len (self.stog):
      return False

    return self.stog[-n]
    
  def prazan (self):
    return len (self.stog) == 0

class Cvor:
  def __init__ (self, nezavrsni, djeca):
    self.nezavrsni = nezavrsni
    self.djeca = djeca

class Produkcija:
  def __init__ (self, lijevo, desno):
    self.lijevo = lijevo
    self.desno = desno

class LRParser:

  def __init__ (self, niz, tablice_path, sinkro_path):
    self.niz = niz
    self.index_niza = 0
    self.stog = Stog()
    self.stog.push ('0')

    self.ucitaj_tablice (tablice_path)
    
    #print self.novaStanja
    #self.akcije = akcije
    
    self.ucitaj_sinkro (sinkro_path)

  def ucitaj_sinkro (self, path):
    fin = open (path, 'r')
    for line in fin:
      if line.startswith ('%Syn'):
        self.sinkro = line[5:].split (' ')
        break
    
  def ucitaj_tablice (self, path):
    tablice_raw = open (path, 'r')
    self.akcije = {}
    self.novaStanja = {}
    
    tablica = ''
    for line in tablice_raw:
      if line.find ('Akcije') != -1 and line[0] == '%':
        tablica = 'akcije'
        continue
      elif line.find ('NovoStanje') != -1 and line[0] == '%':
        tablica = 'novoStanje'
        continue

      (s, z, a) = eval (line)
      if tablica == 'akcije':
        self.akcije[(s, z)] = a
      elif tablica == 'novoStanje':
        self.novaStanja[(s,z)] = a
      else:
        print ('greska')
        sys.exit(-1)
  
  def kraj_niza (self):
    return len (self.niz) < self.index_niza + 1

  def procitaj (self):
    if self.kraj_niza() == True:
      return False

    char = self.niz[self.index_niza]
    self.index_niza += 1
    return char
  
  def pomakni (self, znak, stanje):
    self.stog.push (znak)
    self.stog.push (stanje)
    self.index_niza += 1

  def reduciraj (self, prijelaz):
    ## prijelaztmp = prijelaz.replace(' ', '').split('->')
    ## trenutno_stanje = self.stog.vrh()
    ## lijevo = prijelaztmp[0]
    ## desno = prijelaztmp[1]
    lijevo = prijelaz.lijevo
    desno = prijelaz.desno
    djeca = []

    
    #print "stog5: " + str(self.stog.stog)
    #print "Desno: ", desno
    if '$' not in desno:
      for i in range (len(desno)):
        a = self.stog.pop()
        #print "Izbacio " , a
        znak = self.stog.pop()
        #print "Izbacio " , znak
        if znak == False:
          break
        djeca.append(znak)

      djeca.reverse()

    else:  #epsilon
      djeca = ['$']
     
    #print "stog6: " + str(self.stog.stog)

    cvor = Cvor (lijevo, djeca)
    #print "Cvor: " + str(cvor.nezavrsni) + ' -> ' + str (cvor.djeca)
    self.stog.push (cvor)
    #print "stog0: " + str(self.stog.stog)
    #print 'djeca: ' + str(djeca) 
    novoStanje_raw = self.novaStanja[(self.stog.dohvati (2), cvor.nezavrsni)]
    if novoStanje_raw.find("Stavi") != -1:
      novoStanje = novoStanje_raw[6:-1]
    elif novoStanje_raw.find("Odbaci") != -1:
      self.odbaci ()

    self.stog.push (novoStanje)
  
  def prihvati (self):
    print 'prihvacam'

  def odbaci (self):
    print 'ne prihvacam'

  def analiziraj (self):
    
    while True:
      if self.index_niza +1 > len(self.niz):
        ulaz_char='%'
      else:
        ulaz_char = self.niz[self.index_niza]
      trenutno_stanje = self.stog.vrh()

      akcija = self.akcije.get((trenutno_stanje, ulaz_char), 'Odbaci')
      print "znak:" + ulaz_char
      print "trenutno stanje:" + str(trenutno_stanje)
      print "akcija:" + str(akcija)
      print "stog:" + str(self.stog.stog), '\n'

      if akcija.find ('Reduciraj') != -1:
        prod = eval (akcija[10:-1])
        print "Produkcija: " , prod
        prod = prod.split('->')
        produkcija = Produkcija (prod[0].strip(), prod[1].strip().split(' '))
        self.reduciraj (produkcija)
      elif akcija.find ('Pomakni') != -1:
        self.pomakni (ulaz_char, akcija[8:-1])
      elif akcija.find ('Prihvati') != -1:
        self.prihvati()

        break;

      elif akcija.find ('Odbaci') != -1:
        self.odbaci()
        self.ispisi_gresku(ulaz_char, trenutno_stanje)
        oporavak_uspio = self.oporavi()
        if not oporavak_uspio:
          break
        
        
      #print "stog2:" + str(self.stog.stog) +'\n\n'
        # oporavak TODO

  def ispisi_gresku (self, znak, stanje):
    print "Neocekivani znak: ", znak, '. Ocekuje se: '
    okZnakovi = set()
    for k in self.akcije:
      #print self.akcije[k]
      (s, z) = k
      akcija = self.akcije.get (k, False)
      if akcija != False and akcija[0] != 'O':
        #print 'Dodajem ', z
        okZnakovi.add(z)
    
    for z in okZnakovi:
      sys.stdout.write (z + ' ') 

    print ''

  def oporavi(self):
    while True:
      if self.index_niza +1 > len(self.niz):
        return False

      z = self.niz[self.index_niza]
      print "Znak: ", z
      if z in self.sinkro:
        break

    while (not self.akcije.get ((self.stog.vrh(), z), False)) and not self.stog.prazan():
      print "stog7: ", self.stog.stog
      self.stog.pop()
      self.stog.pop()
    
    raw_input()
    return True
