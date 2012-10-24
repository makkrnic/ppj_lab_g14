from enka import Enka
import sys
#leksicki analizator

#citanje automata i spremanje u objekte
tablicaPrijelaza = open(r'C:\Users\Niko\Desktop\Faks\5. semestar\PPJ\lab1\tablicaPrijelaza.txt','r')
retci = [redak[:-1] for redak in tablicaPrijelaza.readlines()]
tablicaPrijelaza.close()

i = 0
automati = []
prioritet = 0
while(1):
    stanja = retci[i].split(' ')   #sva interna stanja automata
    i += 1
    pocStanje = retci[i]           #pocetno stanje automata
    i += 1
    prihStanje = retci[i]          #prihvatljivo stanje automata
    i += 1
    prijelazi = {}
    #citanje tablice prijelaza pojedinog automata
    while(1):
        prijelaz = retci[i].split(' ')
        i += 1
        if prijelaz == '***Slijede akcije***':
            break
        prijelazi[(prijelaz[0], prijelaz[1])] = prijelaz[2:]
    #citanje akcija za svaki automat
    akcije = []
    while(1):
        if retci[i] == '***Kraj akcija***':
            break
        akcije.append(retci[i])
        i += 1
    automati.append(Enka(stanja, pocStanje, prihStanje, prijelazi, akcije, prioritet))
    prioritet += 1
listaStanjaLA = retci[i].split(' ')   #stanja LA, prvo je pocetno

#leksicki analiziramo program
ulaz = open(r'C:\Users\Niko\Desktop\Faks\5. semestar\PPJ\lab1\minusKod.txt','r')
program = ulaz.read()
#program = sys.stdin.read()

brRedak = 0
rbrZnak = 0
trenutnoStanje = listaStanjaLA[0]   #trenutno stanje postavljamo u pocetno
tablicaIzlaza = []

while (rbrZnak < len(program)):
    ziviAutomati = []
    niz = []
    for automat in automati:    #pokrecemo sve automate koje mozemo
        if automat.pocetno == trenutnoStanje:
            automat.reset()
            trenutniAutomati.append(automat)
            ziviAutomati.append(automat)
    while (1):
        trenutniZnak = program[rbrZnak]   #ucita znak programa
        imaZivih = 0
        for automat in ziviAutomati:      #obavljamo prijelaze za znak dok postoje zivi
            automat.obavi_prijelaz(trenutniZnak)
            if automat.ziv == True:
                imaZivih = 1
                automat.brojIteracija += 1
            else:
                del ziviAutomati[ziviAutomati.index(automat)]
        if imaZivih == 1:
            niz.append(trenutniZnak)
            rbrZnak += 1
        else:
            break
    #odredjujemo automat(e) koji su u prihvatljom stanju
    for automat in trenutniAutomati:
        if automat.isPrihvatljiv:
            prihvAutomati.append(automat)
            
    if len(prihvAutomati) != 0:
        #odredjujemo prihvatljive automat(e) koji su najduze zivjeli
        maksIteracija = max([automat.brojIteracija for automat in prihvAutomati])
        for automat in prihvAutomati:
            if automat.brojIteracija == maksIteracija:
                najduzeZivjeli.append(automat)
        #odredjujemo koji ce automat izvesti svoje akcije
        if len(najduzeZivjeli) == 1:
            finalniAutomat = najduzeZivjeli[0]
        else:
            najveciPrioritet = min([automat.prioritet for automat in najduzeZivjeli])
            for automat in najduzeZivjeli:
                if automat.prioritet == najveciPrioritet:
                    finalniAutomat = automat
        #obavimo akcije za finalni automat
        for akcija in finalniAutomat.akcije:
            eval(akcija)
    else:
        #postupak oporavka od pogreske
        rbrZnak = rbrZnak - len(niz) + 2
        sys.stderr.write('Greska u redu: ' + str(brRedak) + '\n' + 'Greska u znaku: ' + str(rbrZnak - 1) + '\n' + 'Znak: ' + program[rbrZnak - 1])

#ispis izlaza        
izlaz = ''
for lista in tablicaIzlaza:
    redak = ' '.join(lista) + '\n'
    izlaz = izlaz + redak
 
 izlaznaDatoteka = open(r'C:\Users\Niko\Desktop\Faks\5. semestar\PPJ\lab1\izlaznaDatoteka.txt','w')
 izlaznaDatoteka.write(izlaz)
 #sys.stdout.write(izlaz)