import os
import re
import copy


def pobierz_dane(plik):
    """
    Funkcja zwraca tuplę tupli zawierających dane pobrane z pliku csv
    do zapisania w tabeli.
    """
    dane = []  # deklarujemy pustą listę
    if os.path.isfile(plik):  # sprawdzamy czy plik istnieje na dysku
        with open(plik, "r") as zawartosc:  # otwieramy plik do odczytu
            # i = 0
            for linia in zawartosc:
                linia = linia.replace("\n", "")  # usuwamy znaki końca linii
                linia = linia.replace("\r", "")  # usuwamy znaki końca linii
                linia = re.sub(' +', ' ', linia)  # zamieniamy wiecej niz 1 spacje na pojedyncza
                linia = linia.lstrip()  # usuwamy pierwsza spacje
                # x =  map(int, linia.split(" "))
                # x = list(x)                      # tutaj takie wygibasy żeby dodać czwarta liczbę
                # x.append(i)                      # która jest kolejnością zadań
                dane.append(list(map(int, linia.split(" "))))  # dodajemy elementy do tupli a tuplę do listy
                # i = i + 1                        # i++ zadania są numerowane od 1 do n
    else:
        print("Plik z danymi", plik, "nie istnieje!")
    return list(dane)  # przekształcamy listę na tuplę i zwracamy ją


def johnson(dane, n):
    l = 0
    k = n-1
    N = list(dane)
    G = []

    while len(N) != 0:
        j = min(N)
        i = N.index(j)

        if j[0] < j [1]:
            G.insert(l, j)
            l = l+1
        else:
            G.insert(k, j)
            k = k-1
        N.remove(j)

    return G


def optim(dane, n):
    C1 = dane[0][0]
    C2 = C1 + dane[0][1]

    for i in range (1, n):
        C1 = C1 + dane[i][0]
        C2 = C2 + dane[i][1]

    return max(C1, C2)

def kolej(dane, n):
    y = []
    for i in range (0, n):
        y.append(dane[i][2])

    return y


def zad1(files):
    for i in range(0, len(files)):
        dane = pobierz_dane(files[i])
        n = dane[0][0]
        m = dane[0][1]
        dane = dane[1:]
        j = 1
        for item in dane:
            dane[dane.index(item)] = item[1::2]
            dane[dane.index(item[1::2])].append(j)
            j = j + 1

        szereg = johnson(dane, n)
        wynik = optim(szereg, n)
        ustawienie = kolej(szereg, n)

        print("Wynik dla ", files[i], "jest ", wynik)
        print("W kolejnści ", ustawienie)

        # print(files[i], Cmax(dane, n, m), "n=", n, "m=", m)
        # kombinacje = BF(dane)
        # wynik = []
        # for item in kombinacje:
        #     wynik.append(Cmax(item, n, m))
        # print("opt ", min(wynik))


pliki = ["data001.txt", "data003.txt", "data005.txt"]

zad1(pliki)
