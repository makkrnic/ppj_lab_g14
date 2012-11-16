#klasa za enka
class Enka ():
    ''' Klasa za epsilon NKA simulator '''

    def __init__ (self, pocetno, prihvatljivo, prijelazi, akcije, prioritet):
        self.pocetno = pocetno
        self.prihvatljivo = prihvatljivo
        self.prijelazi = prijelazi # { (stanje, znak) : [stanje] }
        self.akcije = akcije
        self.prioritet = prioritet

    def reset (self):
        self.trenutnaStanja = set ([]).union([self.pocetno])
        self.obavi_prijelaz('eps')
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
        nova= set([])
        for stanje in self.trenutnaStanja:
            self.trenutnaStanja = self.trenutnaStanja - set([stanje])
            novaStanja = self.prijelazi.get ((stanje, znak))
            if novaStanja == None:                
                continue
            nova = nova.union(novaStanja)
        self.trenutnaStanja = nova 
        self.epsilon_okruzenje()

    def isPrihvatljiv (self):
        for stanje in self.trenutnaStanja:
            if stanje == self.prihvatljivo:
                return 1
        return 0

    def ziv (self):
        return bool(self.trenutnaStanja)