#!/usr/bin/env python2
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

class LeksickaJedinka:
  def __init__ (self, uniformniZnak, linija, leksicka_jedinka):
    self.unznak = uniformniZnak
    self.linija = linija
    self.lexjed = leksicka_jedinka

  def __str__ (self):
    return self.unznak + ' ' + str(self.linija) + ' ' + self.lexjed


class LRParser:

  def __init__ (self, ulazni_kod, tablice_path, sinkro_path):
    self.niz = self.ucitaj_kod (ulazni_kod)  # niz leksickih jedinki
    self.index_niza = 0
    self.stog = Stog()
    self.stog.push ('0')

    self.ucitaj_tablice (tablice_path)
    
    #print self.novaStanja
    #self.akcije = akcije
    
    self.ucitaj_sinkro (sinkro_path)
    self.niz_odbijen = None

  def ucitaj_kod (self, kod):
    kod = kod.replace ('\r', '').split('\n')
    cijeli_kod = []
    for line in kod:
      jed = line.split(' ')
      if len (jed) < 3:
        continue
      #print "Dodajem: ", jed
      unznak = jed[0]
      linija = jed[1]
      lexjed = ' '.join (jed[2:])

      # print unznak,linija,lexjed
      # raw_input()
      
      cijeli_kod.append (LeksickaJedinka (unznak, linija, lexjed))
    
    return cijeli_kod

  def ucitaj_sinkro (self, path):
    fin = open (path, 'r')
    self.sinkro = eval (fin.read())
    #for line in fin:
    #  if line.startswith ('%Syn'):
    #    self.sinkro = line[5:].rstrip('\n').split (' ')
    #    break
    
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

  def procitaj (self, pomakni_index = True):
    if self.kraj_niza() == True:
      return LeksickaJedinka ('%', 0, '%') 

    char = self.niz[self.index_niza]
    if pomakni_index:
      self.index_niza += 1
    return char
  
  def pomakni (self, ljedinka, stanje):
    self.stog.push (ljedinka)
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
    # print "stog0: " + str(self.stog.stog)
    # print 'djeca: ' + str(djeca) 
    novoStanje_raw = self.novaStanja[(self.stog.dohvati (2), cvor.nezavrsni)]
    if novoStanje_raw.find("Stavi") != -1:
      novoStanje = novoStanje_raw[7:-2]
    elif novoStanje_raw.find("Odbaci") != -1:
      self.odbaci ()

    self.stog.push (novoStanje)

  def niz_prihvacen (self):
    return self.niz_odbijen != True
  
  def prihvati (self):
    #print 'Stog: ', self.stog.stog
    self.stog.pop()
    self.ispis_stabla (self.stog.pop(), 0)
    if self.niz_odbijen == True:
      self.odbaci()
      return
    #print 'prihvacam'

  def odbaci (self):
    #self.stog.pop()
    #self.ispis_stabla(self.stog.pop(), 0)
    self.niz_odbijen = True
    #print 'ne prihvacam'

  def analiziraj (self):
    #for el in self.niz:
      #pprint.pprint (el)
      #print vars(el)

    #raw_input ()
    while True:
      #raw_input()
      if self.index_niza +1 > len(self.niz):
        ulaz = LeksickaJedinka ('%', 0, '%')
      else:
        ulaz = self.niz[self.index_niza]
      ulaz_char = ulaz.unznak
      
      trenutno_stanje = self.stog.vrh()

      akcija = self.akcije.get((trenutno_stanje, ulaz_char), 'Odbaci')
      #print ''
      #print 'Na indeksu ', str(self.index_niza)
      #print "znak:", vars(ulaz)
      #print "trenutno stanje:" + str(trenutno_stanje)
      #print "akcija:" + str(akcija)
      #print "stog:" + str(self.stog.stog), '\n'
      #print ''
      
      #raw_input()
      if akcija.find ('Reduciraj') != -1:
        prod = eval (akcija[10:-1])
       # print "Produkcija: " , prod
        prod = prod.split('->')
        produkcija = Produkcija (prod[0].strip(), prod[1].strip().split(' '))
        self.reduciraj (produkcija)
      elif akcija.find ('Pomakni') != -1:
        self.pomakni (ulaz, akcija[9:-2])
      elif akcija.find ('Prihvati') != -1:
        self.prihvati()

        break;

      elif akcija.find ('Odbaci') != -1:
        self.odbaci()
        #print 'Stog1: ', self.stog.stog
        self.ispisi_gresku(ulaz, trenutno_stanje)
        
        oporavak_uspio = self.oporavi()
        #print 'Oporavak: ', oporavak_uspio
        #self.
        if not oporavak_uspio:
          # print "end loop"
          break
      
      # print "Kraj? ", self.kraj_niza()
      # if self.kraj_niza():
      #   break
      
    #print '\n\nispis stabla: '
    self.stog.pop()
    self.ispis_stabla(self.stog.vrh(), 0)
    #print "stog2:" + str(self.stog.stog) +'\n\n'
      # oporavak TODO

  def ispisi_gresku (self, znak, stanje):
    print "Neocekivani znak: ", znak.unznak, ' u liniji ', znak.linija, '. Ocekuje se: '
    okZnakovi = set()
    for k in self.akcije:
      #print self.akcije[k]
      (s, z) = k
      akcija = self.akcije.get (k, 'Odbaci')
      if s == stanje and akcija != False and akcija[0] != 'O':
        # print 'Kljuc: ', k
        # print "Akcija: ", akcija
        # print 'Dodajem ', z
        # raw_input()
        okZnakovi.add(z)
    
    for z in okZnakovi:
      sys.stdout.write (z + ' ') 

    print ''

  def ispis_stabla(self, cvor, razina):
    #print 'Cvor: ', cvor
    output = sys.stdout
    if isinstance (cvor, LeksickaJedinka):
      output.write (' ' * razina + str(cvor) + '\n')
      return
    elif isinstance (cvor, Cvor):
      roditelj = cvor.nezavrsni
      djeca = cvor.djeca
      output.write (' ' * razina + str(roditelj) + '\n')
      for dijete in djeca:

        self.ispis_stabla (dijete, razina + 1)
    elif isinstance (cvor, str):
      output.write (' ' * razina + cvor + '\n')
    

  def oporavi (self):
    #self.stog.pop()
    #print '\nU Oporavi() Stog: ', self.stog.stog
    #self.procitaj()
    znak = self.procitaj(False)
    # print 'U Oporavi() znak: ', znak
    # print 'Sinkronizacijski znakovi: ', self.sinkro
    while znak.unznak != '%':
      # print 'Preskacem ', vars(znak)
      # print 'na indeksu', str(self.index_niza)
      if znak.unznak in self.sinkro:
        # print 'gotovo preskakanje'
        break
      self.index_niza += 1
      znak = self.procitaj(False)

    # print "Znak: ", vars(znak)
    # print 'na indeksu: ', str(self.index_niza)
    if znak == False:
      # print 'nema znaka!!!!!'
      return False
    #raw_input()
    #self.stog.pop()
    while not self.stog.prazan():
      stanje = self.stog.vrh()
      #print 'Stanje ', stanje
      #raw_input()
      for (s,z) in self.akcije:
        #if s == stanje or z == znak.unznak:
        #  print "Stanje i znak: ", (s,z)
        #  print 'Trazeno stanje i znak: ', (stanje, znak.unznak)
        #print "Stog; ", self.stog.stog
        if s == stanje and z == znak.unznak:
          #print 'Oporavak uspio'
          # print '\n\n\nIzlazim iz oporavi(). znak: ', vars(self.niz[self.index_niza]), 'Index: ', self.index_niza
          return True
        #else:
        #  #raw_input()
        #  #self.stog.pop() # odbaci stanje s vrha
        #  self.stog.pop() # odbaci leksicku jedinku/cvor
      self.stog.pop()
      self.stog.pop()


    #print "oporavak nije uspio"
    return False




if __name__ == '__main__':
  #ulazni_kod = open('../ulazlink').read()
  
  ulazni_kod = sys.stdin.read()
  parser = LRParser (ulazni_kod, 'tabliceLRparsera.txt', 'sinkronizacijskiZnakovi')
  parser.analiziraj()
  if parser.niz_prihvacen():
    sys.exit (0)
  else:
    sys.exit (1)
