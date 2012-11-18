#pretvanjanje enka u dka
import string

znakoviSifre = list(string.letters + string.digits)

def sifriraj(enka):
    global dictStanja, dictZnakova, dictStanjaObrnuti, dictZnakovaObrnuti
    staraStanja = sorted(list(enka.stanja))
    novaStanja = []
    dictStanja = {}
    dictStanjaObrnuti = {}
    sifraStanja = 'a'
    for stanje in staraStanja:
        dictStanja[stanje] = sifraStanja
        dictStanjaObrnuti[sifraStanja] = stanje
        novaStanja.append(sifraStanja)
        #leksicki povecaj sifru
        sifraStanja = list(sifraStanja)
        indexSifraStanja = len(sifraStanja) - 1
        while sifraStanja[indexSifraStanja] == '9':
            indexSifraStanja -= 1
            if indexSifraStanja == -1:
                break
        if indexSifraStanja == -1:
            sifraStanja = ['a']*(len(sifraStanja) + 1)
        else:
            znakSifraZnaka = sifraStanja[indexSifraStanja]
            sifraStanja[indexSifraStanja] = znakoviSifre[znakoviSifre.index(znakSifraZnaka) + 1]
            sifraStanja = sifraStanja[:indexSifraStanja+1] + ['a']*(len(sifraStanja) - indexSifraStanja - 1)
        sifraStanja = ''.join(sifraStanja)
    
    stariZnakovi = sorted(list(enka.ulazniZnakovi))
    noviZnakovi = []
    dictZnakova = {}
    dictZnakovaObrnuti = {}
    sifraZnaka = 'a'
    for znak in stariZnakovi:
        if znak != '$':
            dictZnakova[znak] = sifraZnaka
            dictZnakovaObrnuti[sifraZnaka] = znak
            noviZnakovi.append(sifraZnaka)
            #leksicki povecaj sifru
            sifraZnaka = list(sifraZnaka)
            indexSifraZnaka = len(sifraZnaka) - 1
            while sifraZnaka[indexSifraZnaka] == '9':
                indexSifraZnaka -= 1
                if indexSifraZnaka == -1:
                    break
            if indexSifraZnaka == -1:
                sifraZnaka = ['a']*(len(sifraZnaka) + 1)
            else:
                znakSifraZnaka = sifraZnaka[indexSifraZnaka]
                sifraZnaka[indexSifraZnaka] = znakoviSifre[znakoviSifre.index(znakSifraZnaka) + 1]
                sifraZnaka = sifraZnaka[:indexSifraZnaka+1] + ['a']*(len(sifraZnaka) - indexSifraZnaka - 1)
            sifraZnaka = ''.join(sifraZnaka)
        else:
            noviZnakovi.append('$')
            dictZnakova['$'] = '$'
    
    stariPrijelazi = dict(enka.prijelazi)
    noviPrijelazi = {}
    for stariKljuc in stariPrijelazi.keys():
        novoStanje = dictStanja[stariKljuc[0]]
        noviZnak = dictZnakova[stariKljuc[1]]
        novaStanjaPrijelaza = [dictStanja[stanje] for stanje in stariPrijelazi[stariKljuc]]
        noviKljuc = (novoStanje, noviZnak)
        noviPrijelazi[noviKljuc] = novaStanjaPrijelaza
    
    stariEpsRjecnik = enka.epsRjecnik
    noviEpsRjecnik = {}
    for stanje in stariEpsRjecnik.keys():
        noviEpsRjecnik[dictStanja[stanje]] = [dictStanja[stavka] for stavka in stariEpsRjecnik[stanje]]
    enka.epsRjecnik = noviEpsRjecnik
    
    for stanje in enka.stanja:
        if stanje == enka.pocetno:
            enka.pocetno = dictStanja[stanje]
    enka.stanja = novaStanja
    enka.ulazniZnakovi = noviZnakovi
    enka.prijelazi = noviPrijelazi
    
    return enka

def pretvoriuDka(enka):
    #print 'usao u pretvoriDka, sifriram'
    enka = sifriraj(enka)
    #print 'sifrirao, gradim dka'
    dkaUlazniZnakovi = enka.ulazniZnakovi
    dkaUlazniZnakovi.remove('$')
    enka.trenutnaStanja = set(enka.epsRjecnik[enka.pocetno])
    dkaStanja = [enka.trenutnaStanja]
    indexTrenStanja = 0
    dkaPrijelazi = {}
    while(1):
        trenutneStavke = dkaStanja[indexTrenStanja]
        
        for znak in dkaUlazniZnakovi:
            enka.trenutnaStanja = trenutneStavke
            enka.obavi_prijelaz(znak)
            noveDkaStavke = enka.trenutnaStanja
            epsStavke = set()
            for stavka in noveDkaStavke:
                epsStavke = epsStavke.union(set(enka.epsRjecnik[stavka]))
            noveDkaStavke = noveDkaStavke.union(epsStavke)
            if noveDkaStavke != set([]):
                if noveDkaStavke not in dkaStanja:
                    dkaStanja.append(noveDkaStavke)
                #izracunaj index novog stanja u listi
                indexNovogStanja = dkaStanja.index(noveDkaStavke)
                dkaPrijelazi[(indexTrenStanja, znak)] = indexNovogStanja # stanje je novo u kontekstu ove iteracije kroz while petlju
                
        indexTrenStanja += 1
        if indexTrenStanja == len(dkaStanja):
            break
    
    #print 'izgradio dka, desifriram'
    #desifriraj 
    novaDkaStanja = []
    for stanje in dkaStanja:
        dkaNoveStavke = set()
        for sifraStanja in stanje:
            dkaNoveStavke.add(dictStanjaObrnuti[sifraStanja])
        novaDkaStanja.append(dkaNoveStavke)
    dkaStanja = novaDkaStanja
    
    noviDkaZnakovi = []
    for znak in dkaUlazniZnakovi:
        noviDkaZnakovi.append(dictZnakovaObrnuti[znak])
    dkaZnakovi = noviDkaZnakovi
    
    noviDkaPrijelazi = {}
    for key in dkaPrijelazi.keys():
        noviDkaPrijelazi[(key[0], dictZnakovaObrnuti[key[1]])] = dkaPrijelazi[key]
    dkaPrijelazi = noviDkaPrijelazi
    
    #print 'desifrirao, izlazim iz pretvorDka'
    '''
    print '-----------DKA----------'
    print '-----STANJA-----'
    for stanje in dkaStanja:
    print stanje
    print '-----POCETNO-----'
    print dkaStanja[0][0]
    print '-----PRIJELAZI-----'
    for key in sorted(dkaPrijelazi.keys()):
    print key, ' ----> ', dkaPrijelazi[key]
    print '\n\n'
    '''
    return [dkaStanja, dkaPrijelazi, dkaUlazniZnakovi]