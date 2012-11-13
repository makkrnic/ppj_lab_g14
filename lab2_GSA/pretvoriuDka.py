#pretvanjanje enka u dka
#izbaciti djelove za prihvatljiva stanja

def pretvoriuDka(enka):
    #pretvarnje enka u nka
    nkaStanja = enka.stanja
    nkaUlazniZnakovi = enka.ulazniZnakovi
    nkaUlazniZnakovi.remove('$')
    enka.epsilon_okruzenje()
    nkaPocetno = enka.trenutnaStanja
    #odredjivanje prihvatljivih
    enka.trenutnaStanja = set([enka.pocetno])
    nkaPrihvatljiva = enka.prihvatljiva
    enka.epsilon_okruzenje()
    for stanje in enka.trenutnaStanja:
        if stanje in enka.prihvatljiva:
            nkaPrihvatljiva = nkaPrihvatljiva.union([enka.pocetno])
            break
    
    #odredjivanje prijelaza
    nkaPrijelazi = {}
    for stanje in enka.stanja:
        for znak in enka.ulazniZnakovi:
            if znak != '$':
                enka.trenutnaStanja = set([stanje])
                enka.epsilon_okruzenje()
                #if stanje == nkaPocetno and znak == 'c':
                    
                enka.obavi_prijelaz(znak)
                nkaNovaStanja = enka.trenutnaStanja
                nkaPrijelazi[(stanje, znak)] = nkaNovaStanja
    '''
    print '-----------NKA----------'
    print 'STANJA'
    for stanje in nkaStanja:
        print stanje
    print '------ULAZNI ZNAKOVI-----'
    print nkaUlazniZnakovi
    print 'PRIJELAZI'
    for key in sorted(nkaPrijelazi.keys()):
        print key, '  --->   ', nkaPrijelazi[key]
    '''
    #pretvaranje nka u dka
    dkaPocetno = list(nkaPocetno)
    dkaStanja = []
    dkaPrijelazi = {}
    skupNeobradjenihStanja = []
    dkaPrihvatljiva = set()
    imeStanja = 0
    dkaStavke = dkaPocetno
    pomocnaStanja = []
    while(1):
        dkaStanja.append(dkaStavke)
        pomocnaStanja.append([imeStanja, dkaStavke])
        for stavka in dkaStavke:
            if stavka in nkaPrihvatljiva:
                dkaPrihvatljiva.add(tuple(dkaStavke))
                break
        for znak in nkaUlazniZnakovi:
            dkaNoveStavke = []
            for stavka in dkaStavke:
                for stavka1 in nkaPrijelazi[(stavka, znak)]:
                    if stavka1 not in dkaNoveStavke:
                        dkaNoveStavke.append(stavka1)
                if dkaNoveStavke not in skupNeobradjenihStanja and dkaNoveStavke not in dkaStanja and dkaNoveStavke != []:
                    skupNeobradjenihStanja.append(dkaNoveStavke)
            if dkaNoveStavke != []:
                dkaPrijelazi[(tuple(dkaStavke), znak)] = dkaNoveStavke
        if skupNeobradjenihStanja == []:
            break
        else:
            skupNeobradjenihStanja.reverse()
            dkaStavke = skupNeobradjenihStanja.pop()
            skupNeobradjenihStanja.reverse()
            imeStanja += 1
    #sredjivanje dka podataka
    dkaStanja = pomocnaStanja
    pomocnaPrihvatljiva = list(dkaPrihvatljiva)
    dkaPrihvatljiva = []
    for stanje in dkaStanja:
        if dkaPocetno == stanje[1]:
            dkaPocetno = stanje[0]
        for prihStanje in pomocnaPrihvatljiva:
            if list(prihStanje) == stanje[1]:
                dkaPrihvatljiva.append(stanje[0])
    pomocniPrijelazi = dict(dkaPrijelazi)
    dkaPrijelazi = {}
    for key in pomocniPrijelazi.keys():
        stavke = list(key[0])
        noveStavke = pomocniPrijelazi[key]
        for stanjeDka in dkaStanja:
            if stavke == stanjeDka[1]:
                stanje = stanjeDka[0]
            if noveStavke == stanjeDka[1]:
                novoStanje = stanjeDka[0]
        dkaPrijelazi[(stanje, key[1])] = novoStanje
    dkaUlazniZnakovi = nkaUlazniZnakovi
    
    
    '''
    print '-----------DKA----------'
    print '-----STANJA-----'
    for stanje in dkaStanja:
        print stanje
    print '-----POCETNO-----'
    print dkaPocetno
    print '-----PRIJELAZI-----'
    for key in sorted(dkaPrijelazi.keys()):
        print key, '   ---->   ', dkaPrijelazi[key]
    dkaUlazniZnakovi = nkaUlazniZnakovi
    print '\n\n'
    '''
    return [dkaStanja, dkaPrijelazi, dkaUlazniZnakovi]