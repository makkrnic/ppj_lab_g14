#!/usr/bin/env python

class Re2enka ():

  def __init__ (self, re, pStanje):
    self.ciljno = 2
    self.zadnje_stanje = 5
    self.prijelazi = {}
    self.zadnjiOper = None

    self.pocetno = pStanje
    self.stanja = set([self.pocetno, self.ciljno])
    self.re2enka2 (re, self.pocetno, self.ciljno)
    
    #print ('prijelazi: ' + str(self.prijelazi) + '\n')

    
    while True:
      provjereno_prijelaza = 0
      for p in self.prijelazi:
        provjereno_prijelaza += 1
        (s, z) = p
        if z != 'eps' and len(z) > 1 and z[0] != '\\':
          #print ('prijelaz: ' + str (p) + ' => ' + str(self.prijelazi[p]) + ' nije ok')
          #print ('nije ok')
          self.popravi_prijelaz (p, self.prijelazi[p])
          break
        #else:
        #  #debug
        #  print ('ok')
      
      if provjereno_prijelaza == len (self.prijelazi):
        break
    
    print ('prijelazi Novi: ' + str(self.prijelazi) + '\n')
  
  def novo_stanje (self):
    self.stanja.add(self.zadnje_stanje)
    self.zadnje_stanje += 1
    return self.zadnje_stanje - 1


  def flatten(self, x):
      result = []
      for el in x:
          if hasattr(el, "__iter__") and not isinstance(el, str):
              result.extend(self.flatten(el))
          else:
              result.append(el)
      return result
  
  def dodaj_prijelaz (self, stanje, znak, novo_stanje):
    if not znak:
      znak = 'eps'
      return
    
    #print ('Dodajem: ' + str((stanje, znak)) + ' => ' + str (novo_stanje))

    if (stanje, znak) not in list (self.prijelazi.keys()):
      novo_stanje = [novo_stanje]
      self.prijelazi[(stanje, znak)] = self.flatten(novo_stanje)
    else:
      self.prijelazi[(stanje, znak)].append (novo_stanje)
 
  def popravi_prijelaz (self, prijelazIz, prijelazU):
    #print ('popravljam prijelaz: ' + str (prijelazIz) + ' => ' + str(prijelazU))

    (stanjeIz, znak) = prijelazIz
    stanjaU = prijelazU
    #print ('Brisem: ' + str (prijelazIz) + ' => ' + str(self.prijelazi[prijelazIz]))
    del self.prijelazi[prijelazIz]
    #print ('Prijelazi temp: ' + str (self.prijelazi))
    #print ('Rjesavam regex: ' + znak + '\n')
    
    #print ('Ulazi u re2enka2: '+ str(znak) + ', ' + str (stanjeIz) + ', '+ str(stanjaU) + '\n')
    self.re2enka2 (znak, stanjeIz, stanjaU)
  
  
  def re2enka2 (self, re, pStanje, cStanje):
    #print ('regex: ' + re + '\nPocetno: ' + str(pStanje) + '\nCiljno: ' + str (cStanje) + '\n')
    posebni = ['|', '(', ')', '*']
    posebni2 = {'_': ' ', 'n': "\n", 't': "\t", '$': ''}
  
  
  #  stanja = set ([1])
    
    reList = list()
    i = 0
    while len(re) - 1 >= i:
      if (re[i] == '\\'):
        reList.append (re[i:i+2])
        i += 1
      else:
        reList.append (re[i])
      i += 1

    lijevo = list()
    desno = list()
    
    brZagrada = 0
    i = 0
    dirty = False
    while len(reList) - 1 >= i:
      if reList[i] == '(':
        brZagrada += 1
      elif reList[i] == ')':
        brZagrada -= 1
  
      lijevo.append (reList[i])
  
      if (brZagrada == 0):
        if lijevo[0] == '(':
          lijevo = lijevo[1:-1]
        
        if len(reList) -1 <= i:
          #s1 = self.novo_stanje()
          #print ('zadnji: ' + self.zadnjiOper)
          #print ('desno:')
          #print (desno)
          #if self.zadnjiOper == '':
            #self.prijelazi[(cStanje, ''.join(lijevo))] = [s1]

          #print ('Ciljno: ' + str (cStanje))
          self.dodaj_prijelaz (pStanje, ''.join(lijevo), cStanje)
          break 

        elif reList[i+1] == '*':
          i += 2
          desno = reList[i:]
          # prijelaz za kleena
  
          s1 = self.novo_stanje()
          self.dodaj_prijelaz (pStanje, 'eps', s1)
          self.dodaj_prijelaz (pStanje, 'eps', cStanje)
          s2 = self.novo_stanje()
          self.dodaj_prijelaz (s1, ''.join(lijevo), s2)
          self.dodaj_prijelaz (s2, 'eps', cStanje)
          self.dodaj_prijelaz (cStanje, 'eps', s1)
          s3 = self.novo_stanje()
          self.dodaj_prijelaz (cStanje, ''.join(desno), s3)

          if len (lijevo) > 1:
            self.popravi_prijelaz ((s1, ''.join(lijevo)), s2)

#          if len (desno) > 1:
#            self.popravi_prijelaz ((cStanje, ''.join(desno)), s3)

          self.zadnjiOper = '*'
        elif reList[i+1] == '|':
          i += 2
          desno = reList[i:]
          # prijelaz za ili
          self.dodaj_prijelaz (pStanje, ''.join(lijevo), cStanje)
          self.dodaj_prijelaz (pStanje, ''.join(desno), cStanje)
          
          if len (lijevo) > 1:
            self.popravi_prijelaz ((pStanje, ''.join(lijevo)), cStanje)
          #if len (desno) > 1:
          #  self.popravi_prijelaz ((pStanje, ''.join(desno)), cStanje)
          self.zadnjiOper = '|'
        else:
          #nadovezivanje
          i += 1
          desno = reList[i:]
          s1 = self.novo_stanje()
          self.dodaj_prijelaz (pStanje, ''.join(lijevo), s1)
          self.dodaj_prijelaz (s1, ''.join(desno), cStanje)
          
          if len (lijevo) > 1:
            self.popravi_prijelaz ((pStanje, ''.join(lijevo)), s1)

          #if len (desno) > 1:
          #  self.popravi_prijelaz ((s1, ''.join(desno)), cStanje)
          self.zadnjiOper = ''
        
       # if len (lijevo) < 2:
       #   staroCiljno = self.ciljno
       #   print ('staro ciljno: ' + str (staroCiljno))
       #   self.ciljno = self.novo_stanje()
       #   self.re2enka2 (''.join(desno), staroCiljno, self.ciljno)
       #   #self.popravi_prijelaz ((s1, ''.join(desno), cStanje))
        #self.dodaj_prijelaz (self.ciljno, 'eps', self.novo_stanje())
        #self.dodaj_prijelaz (self.ciljno, ''.join(desno), self.novo_stanje())
        #self.popravi_prijelaz ((self.ciljno, ''.join(desno)), self.zadnje_stanje)


        #novo_ciljno = self.novo_stanje()
        #self.re2enka2 (''.join(desno), self.ciljno, novo_ciljno)
        
  
        break
      
      i += 1
  
def re2enka (re, pocetno):
  r2e = Re2enka(re, pocetno)
  return 
  
