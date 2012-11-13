#klasa za enka
class Enka ():
  ''' Klasa za epsilon NKA simulator '''

  def __init__ (self, stanja, pocetno, prihvatljiva, prijelazi, akcije, prioritet):
    self.stanja         = stanja        # set([])
    self.pocetno        = pocetno
    self.prihvatljiva   = set (prihvatljiva)
    self.prijelazi      = prijelazi     # { (stanje, znak) : [stanje] }
    self.akcije = akcije
    self.prioritet = prioritet


  def reset (self):
    self.trenutnaStanja = set ([]).union([self.pocetno])
    self.epsilon_okruzenje()
    self.brojIteracija = 0
    
  def epsilon_okruzenje (self):
    while True:
      ts = self.trenutnaStanja
      for stanje in self.trenutnaStanja:
        novaStanja = self.prijelazi.get ((stanje, 'eps'))
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

  def isPrihvatljiv (self):
    return bool (self.trenutnaStanja & self.prihvatljiva)

  def ziv (self):
    return bool (self.trenutnaStanja)
