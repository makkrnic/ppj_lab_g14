#pretvaranje dka u tablicu LR(1) parsera

def izradiLRtablicu(dkaStanja, dkaPrijelazi, dkaUlazniZnakovi, zavrsniZnakovi, nezavrsniZnakovi, pocetniNezavrsniZnak, produkcije):
    NovoStanje = {}
    Akcija = {}
    oznakaKrajaNiza = '%'
    #print dkaStanja
    for stanjeZnak in dkaPrijelazi.keys():
        stanje = stanjeZnak[0]
        for stanjeDka in dkaStanja:
            if stanjeDka[0] == stanje:
                stavke = stanjeDka[1]
        znak = stanjeZnak[1]
        if znak in nezavrsniZnakovi:    #tablica NovoStanje
            #ppj knjiga 151.str 4.a)
            NovoStanje[(stanje, znak)] = 'Stavi(' + str(dkaPrijelazi[stanjeZnak]) + ')'
    
    #tablica Akcija
    #print dkaStanja
    for stanjeDka in dkaStanja:
        for stavka in stanjeDka[1]:
            stanje = stanjeDka[0]
            stavka = stavka.split('->')
            lijevaStrana = stavka[0]    #nezavrsni znak na lijevoj strani produkcije
            desno = stavka[1].split(' ')
            desnaStrana = desno[0][:-1]  #desna strana produkcije
            viticastiZnakovi = desno[1][1:-1].split(',') #skup zavrsnih znakova npr. {a1,a2,a3} se sprema u [a1,a2,a3]
            okoTocke = desnaStrana.split('.') #[<string>, <string>]
            #print desnaStrana, okoTocke
            lijevoOdTocke = okoTocke[0][:-1].split('|')
            desnoOdTocke = okoTocke[1][1:].split('|')
            '''
            print lijevaStrana
            print desnaStrana
            print lijevoOdTocke
            print desnoOdTocke
            print viticastiZnakovi
            '''
            #print stanje, desnoOdTocke
            #print viticastiZnakovi, [oznakaKrajaNiza], len(desnoOdTocke)
            #ppj knjiga 151.str 3.a)
            #print lijevaStrana, pocetniNezavrsniZnak, lijevoOdTocke[0], nezavrsniZnakovi[0], viticastiZnakovi, [oznakaKrajaNiza]
            if desnoOdTocke != ['']:
                znakStavke = desnoOdTocke[0]
                if znakStavke in zavrsniZnakovi:
                    Akcija[(stanje, znakStavke)] = 'Pomakni(' + str(dkaPrijelazi[(stanje, znakStavke)]) + ')'
            #ppj knjiga 151.str 3.c)
            #pripaziti na [nezavrsniZnakovi[0]]]------------!!!!!!!!!!!!!!!!!!!!--------------
            elif lijevaStrana == pocetniNezavrsniZnak and lijevoOdTocke[0] == nezavrsniZnakovi[0] and viticastiZnakovi == [oznakaKrajaNiza]:
                Akcija[(stanje, oznakaKrajaNiza)] = 'Prihvati()'
            #ppj knjiga 151.str 3.b)
            else:
                for viticastiZnak in viticastiZnakovi:
                    #razrjesavanje nejednoznacnosti
                    trenutnaProdukcija = [lijevaStrana, lijevoOdTocke]
                    zapisiuTablicu = 1
                    if (stanje, viticastiZnak) in Akcija.keys():
                        zapisiuTablicu = 0
                        
                        if Akcija[stanje, viticastiZnak][0] == 'R': #ako vec postoji akcija reduciraj
                            #nadjiPoziciju trenutneProdukcije u ulaznoj datoteci
                            rbrTrenutneProdukcije = 0
                            for produkcija in produkcije: #[[lijevastranaProd, [desnastranaProd]]]
                                if trenutnaProdukcija == produkcija:
                                    break
                                else:
                                    rbrTrenutneProdukcije += 1
                            #nadjiPoziciju vecZapisaneProdukcije u ulaznoj datoteci
                            rbrStareProdukcije = 0
                            lijevaStranaStareP = Akcija[(stanje, viticastiZnak)].split(' ')[0]
                            desnaStranaStareP = Akcija[(stanje, viticastiZnak)].split(' ')[2:]
                            staraProdukcija = [lijevaStranaStareP, desnaStranaStareP]
                            for produkcija in produkcije: #[[lijevastranaProd, [desnastranaProd]]]
                                if staraProdukcija == produkcija:
                                    break
                                else:
                                    rbrStareProdukcije += 1
                            if rbrTrenutneProdukcije > rbrStareProdukcije:
                                zapisiuTablicu = 1
                    if zapisiuTablicu == 1:
                        desnaStranaProdukcije = ' '.join(lijevoOdTocke)
                        if desnaStranaProdukcije == '':
                            desnaStranaProdukcije = '$'
                        Akcija[(stanje, viticastiZnak)] = 'Reduciraj(' + lijevaStrana + ' -> ' + desnaStranaProdukcije + ')'
    
    #ppj knjiga 151.str 5)
    #svi ostali elementi tablice su Odbaci()
    #unosenje Odbaci u tablicu Akcija
    for stanje in [stanjeDka[0] for stanjeDka in dkaStanja]:
        for znak in zavrsniZnakovi + [oznakaKrajaNiza]:
            if (stanje, znak) not in Akcija.keys():
                Akcija[(stanje, znak)] = 'Odbaci()'
    #unosenje Odbaci u tablicu NovoStanje
    for stanje in [stanjeDka[0] for stanjeDka in dkaStanja]:
        for znak in nezavrsniZnakovi:
            if (stanje, znak) not in NovoStanje.keys():
                NovoStanje[(stanje, znak)] = 'Odbaci()'
    
    #ppj knjiga 151.str 6) - nesto??????????????
    '''
    print '---------Akcija--------'
    for key in sorted(Akcija.keys()):
        print key, Akcija[key]
    print '----------NovoStanje-------'
    for key in sorted(NovoStanje.keys()):
        print key, NovoStanje[key]
    '''
    
    return [Akcija, NovoStanje]