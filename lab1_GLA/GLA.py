#generator leksickog analizatora
import pseudokod
import sys

#citanje ulaza
#ulaz = open(r'C:\Users\Niko\Desktop\Faks\5. semestar\PPJ\lab1\minusLang.txt','r')
#ulaznaDatoteka = ulaz.readlines()
#ulaz.close()
ulaznaDatoteka = sys.stdin.readlines()


#ucitavanje regularnih definicija (do prvog znaka %) 
regDef=[]
i = 0
redak = ulaznaDatoteka[i]
while (redak[0] != "%"):
    regDef.append(redak[:-1].split(' '))
    i += 1
    redak = ulaznaDatoteka[i]
    
#spremanje regularnih definicija u rjecnik i zamjena referenci sa cistim izrazima
# rjecnik  - {imeRegularneDefinicije: regularniIzraz}    
rjecnikRegIzraza = {}
listaReferenci = []    
for definicija in regDef:
    imeRegDef = definicija[0]
    regIzraz = definicija[1]
    for imeRegDefPom in listaReferenci:
        regIzraz = regIzraz.replace(imeRegDefPom, "(" + rjecnikRegIzraza[imeRegDefPom] + ")")
    
    listaReferenci.append(imeRegDef)
    rjecnikRegIzraza[imeRegDef]=regIzraz
   
'''for kljuc in rjecnikRegIzraza.keys():  #cisto print za provjeru
    print kljuc, rjecnikRegIzraza[kljuc]'''

#lista stanja leksickog analizatora
listaStanjaLA = redak[3:-1].split(' ')
i = i + 1
redak = ulaznaDatoteka[i]
#lista imena leksickih jedinki
listaLeksJedinki = redak[3:-1].split(' ')
i = i + 1
redak = ulaznaDatoteka[i]

'''
print listaStanjaLA   #print za provjeru
print listaLeksJedinki'''

tablicaPrijelaza = open(r'analizator/tablicaPrijelaza.txt','w')
while (1):
    stanje = redak [1:redak.find('>')]
    regIzraz = redak[redak.find('>')+1:-1]
    for imeRegDefPom in listaReferenci: #rjesavanje referenci u pravilima
        regIzraz = regIzraz.replace(imeRegDefPom, "(" + rjecnikRegIzraza[imeRegDefPom] + ")")
    
    auto = pseudokod.Automat()   #stvaram objekt automat
    automatInfo = pseudokod.pretvori(regIzraz, auto)    #radim automat iz regIzraza
    pseudokod.dodaj_epsilon_prijelaz(auto, stanje, automatInfo[0])
    
    #zapisujemo automate u datoteku za LA
    tablicaPrijelaza.write(str(stanje) + '\n')               #pocetno stanje
    tablicaPrijelaza.write(str(automatInfo[1]) + '\n')       #onda prihvatljivo stanje
    
    for kljuc in auto.prijelazi.keys():
        tablicaPrijelaza.write(str(kljuc[0]) + ' ' + str(kljuc[1]) + ' ' + ' '.join([str(stanje) for stanje in auto.prijelazi[kljuc]]) + '\n')    #prijelazi u obliku: stanje znak s1 s2...

    tablicaPrijelaza.write('***Slijede_akcije***\n')
    i += 2 #preskacemo "{"
    redak = ulaznaDatoteka[i]
    #pisemo akcije u tablicu u obliku python koda
    znakPostoji = 0
    if redak[:-1] == '-':
        None
    else:
        uniformniZnak = redak[:-1]
        znakPostoji = 1
    i += 1
    noviRedak = 0
    redak = ulaznaDatoteka[i]
    while(redak[0] != '}'):  
        #akcija VRATI SE
        if redak[:-1].split(' ')[0] == 'VRATI_SE':
            tablicaPrijelaza.write('rbrZnak - len(niz) + ' + redak[:-1].split(' ')[1] + '\n')
            tablicaPrijelaza.write('niz[0:' + redak[:-1].split(' ')[1] + ']\n')
        #akcija NOVI REDAK       
        elif redak[:-1] == 'NOVI_REDAK':           
            tablicaPrijelaza.write('brRedak + 1\n')
            noviRedak = 1
        #akcija UDJI U STANJE
        elif redak[:-1].split(' ')[0] == 'UDJI_U_STANJE':
            tablicaPrijelaza.write('"' + redak[:-1].split(' ')[1] + '"\n')
        
        i += 1
        redak = ulaznaDatoteka[i] 
    if znakPostoji == 1:    
        if noviRedak == 0:  #ako nije bilo novog retka
            tablicaPrijelaza.write('tablicaIzlaza.append(["' + uniformniZnak + '", str(brRedak), "".join(niz[0:finalniAutomat.brojIteracija])])\n')
        else:    #ako je bilo novog retka, treba smanjit broj redaka za 1
            tablicaPrijelaza.write('tablicaIzlaza.append(["' + uniformniZnak + '", str(brRedak-1), "".join(niz[0:finalniAutomat.brojIteracija])])\n')
    tablicaPrijelaza.write('***Kraj_akcija***\n')
    
    if i == len(ulaznaDatoteka)-1:
        break
    i += 1
    redak = ulaznaDatoteka[i]
#stavimo i listu svih stanja u datoteku    
tablicaPrijelaza.write('***Kraj_automata***\n')
tablicaPrijelaza.write(' '.join(listaStanjaLA) + '\n')