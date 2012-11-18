#generator sintaksnog analizatora
import sys

from napraviEnka import napraviEnka
from pretvoriuDka import pretvoriuDka
from izradiLRtablicu import izradiLRtablicu

#ucitavanje ulazne datoteke
#ulaz = [redak[:-1] for redak in sys.stdin.readlines()]
ulaznaDatoteka = open(r"test.san", 'r')
ulaz = [redak[:-1] for redak in ulaznaDatoteka.readlines()]
ulaznaDatoteka.close()

#ucitavanje podataka u varijable
nezavrsniZnakovi = ulaz[0][3:].split(' ')
zavrsniZnakovi = ulaz[1][3:].split(' ')
sinkronizacijskiZnakovi = ulaz[2][5:].split(' ')
produkcije = {}
listaProdukcija = []
for redak in ulaz[3:]:
    if redak[0] == '<':
        lijevaStrana = redak
        if lijevaStrana not in produkcije.keys():
            produkcije[redak] = []
    else:
        produkcije[lijevaStrana].append(redak[1:].split(' '))
        listaProdukcija.append([lijevaStrana, redak[1:].split(' ')])
#dodavanje novog pocetnog nezavrsnog znaka u produkcije
pocetniZnak = '<' + nezavrsniZnakovi[0][1:-1] + "'>"
produkcije[pocetniZnak] = [[nezavrsniZnakovi[0]]]
'''
print nezavrsniZnakovi
print zavrsniZnakovi
print sinkronizacijskiZnakovi
print produkcije
'''

enka = napraviEnka(produkcije, nezavrsniZnakovi, zavrsniZnakovi, pocetniZnak)
dka = pretvoriuDka(enka)
tablice = izradiLRtablicu(dka[0], dka[1], dka[2], zavrsniZnakovi, nezavrsniZnakovi, pocetniZnak, listaProdukcija)

Akcija = tablice[0]
NovoStanje = tablice[1]
tabliceLRparsera = open(r'analizator/tabliceLRparsera.txt', 'w')
tabliceLRparsera.write('% Akcije\n')
for stanjeZnak in sorted(Akcija.keys()):
    tabliceLRparsera.write('("' + str(stanjeZnak[0]) + '", "' + stanjeZnak[1] + '", "' + \
    Akcija[stanjeZnak][0:Akcija[stanjeZnak].index('(')+1] + "'" + Akcija[stanjeZnak][Akcija[stanjeZnak].index('(')+1:-1] + "')\")" + '\n')
tabliceLRparsera.write('% NovoStanje\n')
for stanjeZnak in sorted(NovoStanje.keys()):
    tabliceLRparsera.write('("' + str(stanjeZnak[0]) + '", "' + stanjeZnak[1] + '", "' + \
    NovoStanje[stanjeZnak][0:NovoStanje[stanjeZnak].index('(')+1] + "'" + NovoStanje[stanjeZnak][NovoStanje[stanjeZnak].index('(')+1:-1] + "')\")" + '\n')
tabliceLRparsera.close()

sinkroFile = open (r'analizator/sinkronizacijskiZnakovi', 'w')
sinkroFile.write (str(sinkronizacijskiZnakovi))
sinkroFile.close()