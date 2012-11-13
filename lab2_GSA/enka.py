#klasa za enka
class Enka ():
    ''' Klasa za epsilon NKA simulator '''

    def __init__ (self, stanja, ulazniZnakovi, pocetno, prihvatljiva, prijelazi):
        self.stanja = stanja
        self.ulazniZnakovi = ulazniZnakovi
        self.pocetno = pocetno
        self.prihvatljiva = set(prihvatljiva)
        self.prijelazi = prijelazi # { (stanje, znak) : [stanje] }
        self.trenutnaStanja = set ([]).union([self.pocetno])

    def reset (self):
        self.trenutnaStanja = set ([]).union([self.pocetno])
        self.obavi_prijelaz('$')
        self.brojIteracija = 0
        
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
        nova= set([])
        for stanje in self.trenutnaStanja:
            self.trenutnaStanja = self.trenutnaStanja - set([stanje])
            novaStanja = self.prijelazi.get ((stanje, znak))
            if novaStanja == None:                
                continue
            nova = nova.union(novaStanja)
        self.trenutnaStanja = nova 
        self.epsilon_okruzenje()