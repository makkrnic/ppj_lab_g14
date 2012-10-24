#generator leksickog analizatora
#citanje ulaza
import sys

ulaz = open(r'C:\Users\Niko\Desktop\Faks\5. semestar\PPJ\lab1\minusLang.txt','r')
ulaznaDatoteka = ulaz.readlines()
#ulaznaDatoteka = sys.stdin.readlines()
ulaz.close()

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

tablicaPrijelaza = open(r'C:\Users\Niko\Desktop\Faks\5. semestar\PPJ\lab1\tablicaPrijelaza.txt','w')
while (1):
    stanje = redak [1:redak.find('>')]
    regIzraz = redak[redak.find('>')+1:-1]
    for imeRegDefPom in listaReferenci: #rjesavanje referenci u pravilima
        regIzraz = regIzraz.replace(imeRegDefPom, "(" + rjecnikRegIzraza[imeRegDefPom] + ")")
    automatInfo = re2enka(regIzraz, stanje)  #automatInfo je tipa [[stanja],pocStanje, prihStanje,{(stanje,znak):[stanja]}]
    #zapisujemo automate u datoteku za LA
    tablicaPrijelaza.write(' '.join().automatInfo[0] + '\n')    #prvo stanja 
    tablicaPrijelaza.write(automatInfo[1] + '\n')               #onda pocetno stanje
    tablicaPrijelaza.write(automatInfo[2] + '\n')               #onda prihvatljivo stanje
    for kljuc in automatInfo[3].keys():
        tablicaPrijelaza.write(kljuc[0] + ' ' + kljuc[1] + ' ' + ' '.join(automatInfo[3][kljuc]) + '\n')    #prijelazi u obliku: stanje znak s1 s2...
    
    tablicaPrijelaza.write('***Slijede akcije***\n')
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
            tablicaPrijelaza.write('rbrZnak = rbrZnak - len(niz) + ' + redak[:-1].split(' ')[1] + '\n')
            tablicaPrijelaza.write('niz = niz[0:' + redak[:-1].split(' ')[1] + ']\n')
        #akcija NOVI REDAK       
        elif redak[:-1] == 'NOVI_REDAK':           
            tablicaPrijelaza.write('brRedak += 1\n')
            noviRedak = 1
        #akcija UDJI U STANJE
        elif redak[:-1].split(' ')[0] == 'UDJI_U_STANJE':
            tablicaPrijelaza.write('trenutnoStanje = ' + redak[:-1].split(' ')[1] + '\n')
        
        i += 1
        redak = ulaznaDatoteka[i] 
    if znakPostoji == 1:    
        if noviRedak == 0:  #ako nije bilo novog retka
            tablicaPrijelaza.write('tablicaIzlaza.append([' + uniformniZnak + ', str(brRedak), niz])\n')
        else:    #ako je bilo novog retka, treba smanjit broj redaka za 1
            tablicaPrijelaza.write('tablicaIzlaza.append([' + uniformniZnak + ', str(brRedak-1), niz])\n')
    tablicaPrijelaza.write('***Kraj akcija***\n')
    
    if i == len(ulaznaDatoteka)-1:
        break
    i += 1
    redak = ulaznaDatoteka[i]
    
tablicaPrijelaza.write(' '.join(listaStanjaLA) + '\n')