import os
import re
import random
import math
import copy
import time
from os import listdir
from os.path import isfile, join
import numpy as np



def pobierz_dane(plik):
    """
    Funkcja zwraca tuplę tupli zawierających dane pobrane z pliku csv
    do zapisania w tabeli.
    """
    #plik = "test_files/" + plik
    dane = []  # deklarujemy pustą listę
    if os.path.isfile(plik):  # sprawdzamy czy plik istnieje na dysku
        with open(plik, "r") as zawartosc:  # otwieramy plik do odczytu
            # i = 0
            for linia in zawartosc:
                linia = linia.replace("\n", "")  # usuwamy znaki końca linii
                linia = linia.replace("\r", "")  # usuwamy znaki końca linii
                linia = re.sub(' +', ' ', linia)  # zamieniamy wiecej niz 1 spacje na pojedyncza
                linia = linia.lstrip()  # usuwamy pierwsza spacje
                linia = linia.rstrip()
                # x =  map(int, linia.split(" "))
                # x = list(x)                      # tutaj takie wygibasy żeby dodać czwarta liczbę
                # x.append(i)                      # która jest kolejnością zadań
                # print(plik[11:len(plik)-4])
                if linia == plik[11:len(plik) - 4]:
                    continue
                if linia == '':
                    continue
                dane.append(list(map(int, linia.split(" "))))  # dodajemy elementy do tupli a tuplę do listy
                # i = i + 1                        # i++ zadania są numerowane od 1 do n
    else:
        print("Plik z danymi", plik, "nie istnieje!")
    return list(dane)  # przekształcamy listę na tuplę i zwracamy ją


def kolejnosc(lista):
    y = []
    m = len(lista[0]) - 1
    for item in lista:
        y.append(item[m])
    return y



def graf_rozwiazania(tab):
    g = []
    n = len(tab)
    m = len(tab[0])-1
    for i in range(0, m):
        g.append([])
        for j in range(0, n):
            g[i].append(tab[j][i])
    return g

def Cmax(tab):
    G = graf_rozwiazania(tab)
    n = len(tab)
    m = len(tab[0]) -1
    C = np.zeros(shape=[len(G), len(G[0])])
    S = np.zeros(shape=[len(G), len(G[0])])  # C i S zerowe macierze o rozmiarach takich jak G
    for i in range(0, m):
        for j in range(0, n):
            S[i][j] = max(C[i][j-1], C[i-1][j]) #j-1, i-1
            C[i][j] = S[i][j] + G[i][j]

    return C[m-1][n-1]
#
# print(Cmax(wlist));
#************************* GOOD

def neh(tab):
    wlist=[];

    for i in range(0, len(tab)):
        wlist.append(sum(tab[i][:-1]))


    good = []

    #print(wlist)
    for i in range(0, len(wlist)):
        a = wlist.index(max(wlist))

        #x = 0
        cemax = 9999
        x = 0

        for j in range(0, len(good)+1):

            tlist = copy.deepcopy(good)
            tlist.insert(j, tab[a])

            cemax2 = Cmax(tlist)

            if cemax2 < cemax:
                cemax = cemax2
                x = j

        good.insert(x, tab[a])
        wlist[a] = 0;

    return good

def zadanie(file):
    wyniki = []
    czasy = []
    for i in range(0, len(file)):
        dane = pobierz_dane(file[i])
        n = dane[0][0]
        m = dane[0][1]
        dane = dane[1:]
        j = 1
        for item in dane:
            dane[dane.index(item)] = item[1::2]
            dane[dane.index(item[1::2])].append(j)
            j = j + 1

        print("################################################")
        start = time.time()
        odp = neh(dane)
        wynik = Cmax(odp)
        permut = kolejnosc(odp)
        end = time.time()

        print("W pliku ", file[i])
        print("Wynik to: ", wynik)
        print("w kolejnosci: ", permut)
        print("w czasie: ", (end-start)*1000)

        wyniki.append(wynik)
        czasy.append(round((end-start)*1000, 3))
        #wynik = Cmax(neh(tab))
        #print(wynik)
        #print(neh(tab))
    print("WYNIKI: ", wyniki)
    print("czasy: ", czasy)


pliki = ["ta001.txt","ta002.txt", "ta003.txt", "ta004.txt", "ta005.txt", "ta006.txt", "ta007.txt", "ta008.txt", "ta009.txt", "ta010.txt"]
pliki2 = ["ta011.txt", "ta021.txt", "ta031.txt", "ta041.txt", "ta051.txt", "ta061.txt", "ta071.txt", "ta081.txt", "ta091.txt", "ta101.txt", "ta111.txt"]
zadanie(pliki)