#leksicki analizator
from enka import Enka
import sys

tablicaPrijelaza = open(r'tablicaPrijelaza.txt','r')
retci = [redak[:-1] for redak in tablicaPrijelaza.readlines()]
tablicaPrijelaza.close()

i = 0
automati = []
prioritet = 0
#citanje automata i spremanje u objekte
while(1):
    pocStanje = retci[i]           #pocetno stanje automata
    i += 1
    if pocStanje == '***Kraj_automata***':
        break
    prihStanje = retci[i]          #prihvatljivo stanje automata
    i += 1
    prijelazi = {}
    #citanje tablice prijelaza pojedinog automata
    while(1):
        prijelaz = retci[i].split(' ')
        i += 1
        if prijelaz == ['***Slijede_akcije***']:
            break
        '''if prijelaz[1]=='' and prijelaz[2]== '': #znak je razmak
            prijelazi[(prijelaz[0], ' ')] = prijelaz[3:]
        else:'''
        prijelazi[(prijelaz[0], prijelaz[1])] = prijelaz[2:] #spremanje tablice prijelaza prijelazi:{(stanje,znak): [stanja]}
    #citanje akcija za svaki automat
    akcije = []
    while(1):
        if retci[i] == '***Kraj_akcija***':
            i += 1
            break
        akcije.append(retci[i])
        i += 1
    automati.append(Enka(pocStanje, prihStanje, prijelazi, akcije, prioritet))
    prioritet += 1
listaStanjaLA = retci[i].split(' ')   #stanja LA, prvo je pocetno

#ulaz = open(r'C:\Users\Niko\Desktop\Faks\5. semestar\PPJ\lab1\minusKod.txt','r')
#program = ulaz.read()
program = sys.stdin.read()

posebniZnakovi = {'\n':'\\n', '\t':'\\t', ' ':'\\_'}
brRedak = 1
rbrZnak = 0
trenutnoStanje = listaStanjaLA[0]   #trenutno stanje postavljamo u pocetno
tablicaIzlaza = []
#leksicki analiziramo program
while (rbrZnak < len(program)):
    ziviAutomati = []
    trenutniAutomati = []
    niz = []
    promijenjenoStanje = 0
    for automat in automati:    #pokrecemo sve automate koje mozemo
        automat.reset()
        if automat.pocetno == trenutnoStanje:            
            trenutniAutomati.append(automat)
            ziviAutomati.append(automat)
    #krecemo sa citanjem programa i radnjom automata
    while (1):
        if rbrZnak == len(program):
            break 
        trenutniZnak = program[rbrZnak]   #ucita znak programa
        if trenutniZnak in posebniZnakovi.keys():   
            trenutniZnak = posebniZnakovi[trenutniZnak]
        imaZivih = 0       
        mrtviAutomati = []
        for automat in ziviAutomati:      #obavljamo prijelaze za sve zive automate za ucitan znak
            trs = automat.trenutnaStanja  
            automat.obavi_prijelaz(trenutniZnak)
            if automat.ziv() == True:
                imaZivih = 1
                automat.brojIteracija += 1
            else:
                automat.trenutnaStanja = trs
                mrtviAutomati.append(automat)

        for automat in trenutniAutomati:      #brise mrtve automate iz liste zivih
            if automat in mrtviAutomati:
                del ziviAutomati[ziviAutomati.index(automat)]
                
        if imaZivih == 1:                 #ako ima zivih, dodajemo znak u niz i citamo sljedeci
            if trenutniZnak == '\_':
                niz.append(' ')
            else:
                niz.append(trenutniZnak)
            rbrZnak += 1
        else:
            break
    
    #odredjujemo automat(e) koji su u prihvatljivom stanju
    prihvAutomati = []
    for automat in trenutniAutomati:
        if automat.isPrihvatljiv():
            prihvAutomati.append(automat)
            
    najduzeZivjeli = []
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
            if akcija.split(' ')[0] == 'brRedak':
                brRedak = eval(akcija)
            elif akcija.split(' ')[0] == 'rbrZnak':
                rbrZnak = eval(akcija)
            elif akcija[0:3] == 'niz':
                niz = eval(akcija)
            elif akcija[0:7] == 'tablica': 
                eval(akcija)
                rbrZnak = rbrZnak - len(niz) +len(niz[0:finalniAutomat.brojIteracija])
            else:
                trenutnoStanje = eval(akcija)
                
    else:
        #postupak oporavka od pogreske
        rbrZnak = rbrZnak - len(niz) + 1
        sys.stderr.write('Greska u redu: ' + str(brRedak) + '\n' + 'Greska u znaku: ' + str(rbrZnak - 1) + '\n' + 'Znak: ' + program[rbrZnak - 1] + '\n')

#ispis izlaza        
izlaz = ''
for lista in tablicaIzlaza:
    redak = ' '.join(lista) + '\n'
    izlaz = izlaz + redak

#izlaznaDatoteka = open(r'C:\Users\Niko\Desktop\Faks\5. semestar\PPJ\lab1\izlaznaDatoteka.txt','w')
#izlaznaDatoteka.write(izlaz)
sys.stdout.write(izlaz)