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

class LRParser:

  def __init__ (self, niz, tablice_path):
    self.niz = niz
    self.index_niza = 0
    self.stog = Stog()
    self.stog.push ('0')

    self.ucitaj_tablice (tablice_path)
    
    #print self.novaStanja
    #self.akcije = akcije
    
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
    return len (self.niz) <= self.index_niza + 1

  def procitaj (self):
    if self.kraj_niza():
      return False

    char = self.niz[self.index_niza]
  
  def pomakni (self, znak, stanje):
    self.stog.push (znak)
    self.stog.push (stanje)
    self.index_niza += 1

  def reduciraj (self, prijelaz):
    prijelaztmp = prijelaz.replace(' ', '').split('->')
    trenutno_stanje = self.stog.vrh()
    lijevo = prijelaztmp[0]
    desno = prijelaztmp[1]
    djeca = []
    
    if len(desno) > 0:
      for i in range (2* len(desno)):
        if i % 2 == 1:
          djeca.append(self.stog.pop())

      djeca.reverse()

    else:  #epsilon
      djeca = ['$']
      
    cvor = Cvor (lijevo, djeca)
    self.stog.push (cvor)
    novoStanje = self.novaStanja[(trenutno_stanje, cvor.nezavrsni)]
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
      print "stog:" + str(self.stog.stog)

      if akcija.find ('Reduciraj') != -1:
        prod = eval (akcija[10:-1])
        #print prod
        self.reduciraj (prod)
      elif akcija.find ('Pomakni') != -1:
        self.pomakni (ulaz_char, akcija[8:-1])
      elif akcija.find ('Prihvati') != -1:
        self.prihvati()
        break
      elif akcija.find ('Odbaci') != -1:
        self.odbaci()
        break;
        
      print "stog2:" + str(self.stog.stog) +'\n\n'
        # oporavak TODO
