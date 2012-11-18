#napravi enka
import racunaZapocinje
from enka import Enka

#klasa za eNka
class Automat:
    def __init__(self, pocetniZnak):
        self.prijelazi = {}
        self.pocetnoStanje = []
        self.svaStanja = []
    
    def dodaj_stanje(self, stanje):
        if stanje not in self.svaStanja:
            self.svaStanja.append(stanje)
      
    def dodaj_epsilon_prijelaz(self, st1, st2):

        if (st1,"$") in self.prijelazi.keys():
            self.prijelazi[(st1,"$")].append(st2)
        else:
            self.prijelazi[(st1,"$")] = [st2]
        
    def dodaj_prijelaz(self, st1, st2, znak):

        if (st1,znak) in self.prijelazi.keys():
            self.prijelazi[(st1,znak)].append(st2)
        else:
            self.prijelazi[(st1,znak)] = [st2]
      

def napraviEnka(produkcije, nezavrsniZnakovi, zavrsniZnakovi, pocetniZnak):
    #napravi zapocinje skupove za svaki znak i svaki sufiks desne strane svake produkcije
    listaPraznih = racunaZapocinje.prazniZnakovi(produkcije) #lista praznih znakova
    zapocinje = racunaZapocinje.zapocinjeZaZnakove(produkcije, nezavrsniZnakovi, zavrsniZnakovi, pocetniZnak) #zapocinje[znak] = [znakovi]
    zapocinjeSufiks = racunaZapocinje.zapocinjeZaSufikse(produkcije, zapocinje) #zapocinjeSufiks[sufiks] =  [znakovi]
    #stvaranje eNKA
    enka = Automat(pocetniZnak)
    
    #stavke za pocetni znak
    pocetnaStavka = [pocetniZnak] + ['->'] + ['.'] + produkcije[pocetniZnak][0] + [',']+ ['{'] +['%'] + ['}']
    enka.pocetnoStanje = pocetnaStavka
    enka.dodaj_stanje(pocetnaStavka)

    '''#iz pocetnog znaka napravi 'eps' prijelaz u sve pripadajuce stavke
    for desnaStrana in produkcije[nezavrsniZnakovi[0]]:
        stavka = [nezavrsniZnakovi[0]]+['->']+['.']+ desnaStrana + [',']+ ['{'] +['%'] + ['}']
        enka.dodaj_stanje(stavka)
        enka.dodaj_epsilon_prijelaz(tuple(enka.pocetnoStanje), stavka)'''
    
    #napravi ostale stavke
    for stanje in enka.svaStanja:
        indeksTocke = stanje.index('.')
        if indeksTocke == stanje.index(',') - 1:
            continue
        #prebaci tocku preko znaka i predji s tim znakom u novu stavku
        znak = stanje[indeksTocke+1]
        stavka = list(stanje)
        stavka[indeksTocke+1] = '.'
        stavka[indeksTocke] = znak
        enka.dodaj_stanje(stavka)
        enka.dodaj_prijelaz(tuple(stanje), tuple(stavka), znak)
        #ako je znak nezavrsan onda pokreni njegovu obradu
        if znak in nezavrsniZnakovi:
            sufiks = stanje[indeksTocke+2:stanje.index(',')]
            skup = stanje[stanje.index('{')+1:stanje.index('}')]
            #novi skup je zapocinje(sufiks)
            noviSkup = []
            if sufiks!=[]:
                noviSkup = zapocinjeSufiks[''.join(sufiks)]
            
            #ako je sufiks niz praznih znakova novom skupu treba dodati stari
            sufiksJePrazan = 1
            for znakSufiksa in sufiks:
                if znakSufiksa not in listaPraznih:
                    sufiksJePrazan = 0
                    break
            if sufiksJePrazan == 1:
                noviSkup = list(set(noviSkup).union(set(skup)))

            for desnaStrana in produkcije[znak]:
                if desnaStrana != ['$']:
                    stavka = [znak] + ['->'] + ['.'] + desnaStrana + [',']+ ['{'] + noviSkup + ['}']
                else:
                    stavka = [znak] + ['->'] + ['.'] + [','] + ['{'] + noviSkup + ['}']
                enka.dodaj_stanje(stavka)
                enka.dodaj_epsilon_prijelaz(tuple(stanje), tuple(stavka))

    #stavke/stanja zapisat kao stringove
    #za pocetno
    skupStr = ', {' + ','.join(enka.pocetnoStanje[enka.pocetnoStanje.index('{')+1:enka.pocetnoStanje.index('}')]) + '}'
    desnoStr = '|'.join(enka.pocetnoStanje[enka.pocetnoStanje.index('->')+1:enka.pocetnoStanje.index(',')]) + skupStr
    pocetnoStr = ''.join(enka.pocetnoStanje[:enka.pocetnoStanje.index('->')+1]) + desnoStr
    
    #za sva stanja
    svaStanjaStr = []
    for stanje in enka.svaStanja:
        skupStr = ', {' + ','.join(stanje[stanje.index('{')+1:stanje.index('}')]) + '}'
        desnoStr = '|'.join(stanje[stanje.index('->')+1:stanje.index(',')]) + skupStr
        stanjeStr = ''.join(stanje[:stanje.index('->')+1]) + desnoStr
        svaStanjaStr.append(stanjeStr)
    
    #za sve prijelaze
    prijelaziStr = {}
    for kljuc in enka.prijelazi:
        skupIZ = ', {' + ','.join(kljuc[0][kljuc[0].index('{')+1:kljuc[0].index('}')]) + '}'
        desnoIZ = '|'.join(kljuc[0][kljuc[0].index('->')+1:kljuc[0].index(',')]) + skupIZ
        stanjeIZ = ''.join(kljuc[0][:kljuc[0].index('->')+1]) + desnoIZ
        prijelaziStr[(stanjeIZ, kljuc[1])] = []
        for stanje in enka.prijelazi[kljuc]:
            skupU = ', {' + ','.join(stanje[stanje.index('{')+1:stanje.index('}')]) + '}'
            desnoU = '|'.join(stanje[stanje.index('->')+1:stanje.index(',')]) + skupU
            stanjeU = ''.join(stanje[:stanje.index('->')+1]) + desnoU
            prijelaziStr[(stanjeIZ, kljuc[1])].append(stanjeU)
    
    
    enka.pocetnoStanje = pocetnoStr  
    enka.svaStanja = svaStanjaStr
    enka.prijelazi = prijelaziStr
    denisEnka = Enka(enka.svaStanja, nezavrsniZnakovi + zavrsniZnakovi + ['$'],enka.pocetnoStanje, enka.svaStanja, enka.prijelazi)
    
            
    '''
    print '---------ENKA---------'
    print 'POCETNO STANJE'
    print enka.pocetnoStanje
    
    print 'STANJA'
    for stanje in enka.svaStanja:
        print stanje
    
    print 'PRIJELAZI'        
    for kljuc in enka.prijelazi.keys():
        print kljuc, '  ->  ', enka.prijelazi[kljuc]
    print '\n\n'
    '''
    
    return denisEnka