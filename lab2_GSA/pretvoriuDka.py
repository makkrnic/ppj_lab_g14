#pretvanjanje enka u dka
#izbaciti djelove za prihvatljiva stanja

def pretvoriuDka(enka):
    dkaUlazniZnakovi = enka.ulazniZnakovi
    dkaUlazniZnakovi.remove('$') #ili ne????????????
    enka.trenutnaStanja = set([enka.pocetno])
    enka.epsilon_okruzenje()
    dkaStanja = [[enka.trenutnaStanja, 1]] #[[set([stavke]), oznaka nekompletnosti]]
    indexTrenStanja = 0
    dkaPrijelazi = {}
    while(1):
        dkaStanja[indexTrenStanja][1] = 0 #nekompletno = 0, tj. stanje je kompletno
        trenutneStavke = dkaStanja[indexTrenStanja][0]
        for znak in dkaUlazniZnakovi:
            enka.trenutnaStanja = trenutneStavke
            enka.obavi_prijelaz(znak)
            noveDkaStavke = enka.trenutnaStanja
            if noveDkaStavke != set([]):
                if noveDkaStavke not in [dkaStanje[0] for dkaStanje in dkaStanja]:
                    dkaStanja.append([noveDkaStavke, 1]) #dodaj U kao nekompletno stanje
                #izracunaj index novog stanja u listi
                for stanje in dkaStanja:
                    if stanje[0] == noveDkaStavke:
                        indexNovogStanja = dkaStanja.index(stanje)
                dkaPrijelazi[(indexTrenStanja, znak)] = indexNovogStanja # stanje je novo u kontekstu ove iteracije kroz while petlju
                
        indexTrenStanja += 1
        if indexTrenStanja == len(dkaStanja):
            break
    
    '''
    print '-----------DKA----------'
    print '-----STANJA-----'
    for stanje in dkaStanja:
        print stanje
    print '-----POCETNO-----'
    print dkaStanja[0][0]
    print '-----PRIJELAZI-----'
    for key in sorted(dkaPrijelazi.keys()):
        print key, '   ---->   ', dkaPrijelazi[key]
    print '\n\n'
    '''
    return [dkaStanja, dkaPrijelazi, dkaUlazniZnakovi]