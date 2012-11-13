#racunanje zapocinje skupova
def prazniZnakovi (produkcije):
    listaPraznih = []
    #dodajemo u listu praznih one znakove koji imaju s desne strane produkcije '$'
    for lijevaStrana in produkcije.keys():
        for desnaStrana in produkcije[lijevaStrana]:
            if desnaStrana == ['$']:
                listaPraznih.append(lijevaStrana)
                break
    
    #dodajemo u listu praznih one znakove kojima su svi znakovi desne strane prazni
    while(1):
        dodanoPraznih = 0
        for lijevaStrana in produkcije.keys():
            jePrazan = 1
            for desnaStrana in produkcije[lijevaStrana]:
                for znak in desnaStrana:
                    if znak not in listaPraznih:
                        jePrazan = 0
                        break
                if (jePrazan == 1) and (lijevaStrana not in listaPraznih):
                    listaPraznih.append(lijevaStrana)
                    dodanoPraznih = 1
                    break 
        if dodanoPraznih == 0:
            break            
    return listaPraznih

def tablicaZapocinjeIzravnoZnakom (produkcije):
    listaPraznih = prazniZnakovi(produkcije)
    zapocinjeIzravnoZnakom = {}
    #u rjecnik se dodaje (lijevaStrana, prviZnakDesneStrane) = 1
    #PONAVLJAJ: ako je taj znak prazan, onda se isto dodaje u rjecnik i za sljedeci znak
    for lijevaStrana in produkcije.keys():
        for desnaStrana in produkcije[lijevaStrana]:
            for znak in desnaStrana:
                if znak != '$':
                    zapocinjeIzravnoZnakom[(lijevaStrana,znak)] = 1
                    if (znak not in listaPraznih):
                        break
    return  zapocinjeIzravnoZnakom

def tablicaZapocinjeZnakom(produkcije, sviZnakovi): 
    zapocinjeIzravnoZnakom = tablicaZapocinjeIzravnoZnakom(produkcije)
    zapocinjeZnakom = {}
    zapocinjeZnakom.update(zapocinjeIzravnoZnakom)
    #refleksivno i tranzitivno okruzenje rjecnika zapocinjeIzravnoZnakom
    while (1):
        dodanZapis = 0
        for znak1 in sviZnakovi:
            zapocinjeZnakom[(znak1,znak1)] = 1
            for znak2 in sviZnakovi:
                for znak3 in sviZnakovi:
                    if zapocinjeZnakom.get((znak1,znak2)) == 1 and zapocinjeZnakom.get((znak2,znak3)) == 1:
                        if zapocinjeZnakom.get((znak1,znak3)) == None:
                            zapocinjeZnakom[(znak1,znak3)] = 1
                            dodanZapis = 1
        if dodanZapis == 0:
            break
    return zapocinjeZnakom                        
                      
def zapocinjeZaZnakove(produkcije, nezavrsniZnakovi, zavrsniZnakovi, pocetniZnak):
    sviZnakovi = nezavrsniZnakovi + zavrsniZnakovi + ['$'] + [pocetniZnak]
    zapocinjeZnakom = tablicaZapocinjeZnakom(produkcije, sviZnakovi)
    zapocinjeSkupovi = {}   #{znak:[lista zavrsnih znakova]}
    #redak tablice tablicaZapocinjeZnakom je skup zapocinje za pripadajuci znak
    for znak1 in sviZnakovi:
        zapocinjeSkupovi[znak1] = []
        for znak2 in zavrsniZnakovi:
            if zapocinjeZnakom.get((znak1,znak2)) == 1:
                zapocinjeSkupovi[znak1].append(znak2) 
    return zapocinjeSkupovi
        
def zapocinjeZaProdukciju(desnaStrana, zapocinjeSkupovi, listaPraznih):
    zapocinje = set([])
    #zapocinje skup produkcije = unija zapocinje skupova svih znakova desne strane produkcije do prvog nepraznog znaka
    for znak in desnaStrana:
        zapocinje = zapocinje.union(zapocinjeSkupovi[znak])   
        if znak not in listaPraznih:
            break
    return list(zapocinje)
               
def zapocinjeZaSufikse(produkcije, zapocinjeSkupovi):
    listaPraznih = prazniZnakovi(produkcije)
    zapocinje = {}
    #radimo zapocinje skupove za sve sufikse desnih strana produkcija
    for lijevaStrana in produkcije.keys():
        for desnaStrana in produkcije[lijevaStrana]: 
            for znak in desnaStrana:
                sufiks = desnaStrana[desnaStrana.index(znak):]
                if zapocinje.get(''.join(sufiks)) == None:
                    zapocinje[''.join(sufiks)] = zapocinjeZaProdukciju(sufiks, zapocinjeSkupovi, listaPraznih)
    return zapocinje