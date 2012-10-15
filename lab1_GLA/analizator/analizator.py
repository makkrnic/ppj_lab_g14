#!/usr/bin/env python
def re2enka (re):
  posebni = ['|', '(', ')', '*', '$']
  posebni2 = {'_': ' ', 'n': "\n", 't': "\t"}

  stanja = set ([1])
  prijelazi = {}

  kleen = False
  ili = False
  slash = False
  stanjaIspredZagrada = []
  prethodnoStanje = None
  prethodnoZagrada = False
  stanje = 1
  zagrade = 0
  for i in range (0, len (re)):
    znak = re[i]
    if znak == '\\' and not slash:
      slash = True
      continue

    if slash and (znak in posebni2):
      znak = posebni2[znak]
    elif not slash and (znak in posebni):
      if znak == '(':
        zagrade += 1
        stanjaIspredZagrada.append (stanje)
        continue
      elif znak == ')':
        zagrade -= 1
        prethodnoZagrada = True
        continue
      elif znak == '*':
        kleen = True
      elif znak == '|':
        ili = True
      
    if prethodnoZagrada:
      prethodnoStanje = stanjaIspredZagrada.pop()
      prethodnoZagrada = False
    else:
      prethodnoStanje = stanje

    stanje += 1
    stanja.add (stanje)

    if kleen:
      kleen = False
      if prijelazi.get((prethodnoStanje, 'eps'), False):
        prijelazi[(prethodnoStanje, 'eps')].append(stanje)
      else:
        prijelazi[(prethodnoStanje, 'eps')] = [stanje]

      continue
      
      

    slash = False

    
    if prijelazi.get((stanje - 1, znak), False):
      prijelazi[(stanje - 1, znak)].append(stanje)
    else:
      prijelazi[(stanje - 1, znak)] = [stanje]
  
  print ('Stanja: '); print (stanja)
  print ('Prijelazi: '); print(prijelazi)
