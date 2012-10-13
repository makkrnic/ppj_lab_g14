#!/usr/bin/env python

class Enka ():
  ''' Glavna klasa '''

  def __init__ (self, stanja, pocetno, prihvatljiva, prijelazi):
    self.stanja         = stanja        # set([])
    self.pocetno        = pocetno
    self.prihvatljiva   = prihvatljiva
    self.prijelazi      = prijelazi     # { (stanje, znak) : [stanje] }

    self.trenutnaStanja = set ([]).union([self.pocetno])


  def epsilon_okruzenje (self):
    while True:
      ts = self.trenutnaStanja
      for stanje in self.trenutnaStanja:
        novaStanja = self.prijelazi.get ((stanje, '$'))
        if novaStanja == None:
          continue

        self.trenutnaStanja = self.trenutnaStanja.union (novaStanja)

      if ts == self.trenutnaStanja:
        break

  def obavi_prijelaz (self, znak):
    for stanje in self.trenutnaStanja:
      self.trenutnaStanja = self.trenutnaStanja - set([stanje])
      
      novaStanja = self.prijelazi.get ((stanje, znak))
      if novaStanja == None:
        continue

      self.trenutnaStanja = self.trenutnaStanja.union (novaStanja)

    self.epsilon_okruzenje()
