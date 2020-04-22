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


def graf_rozwiazania(tab, n, m):
    g = []
    for i in range(0, m):
        g.append([])
        for j in range(0, n):
            g[i].append(tab[j][i])
    return g


def bruteforce(tablica, wynik, krok=0):
    if krok == len(tablica):
        wynik.append(tablica)  # koniec, dodaj permutacje
    for i in range(krok, len(tablica)):
        tablica_copy = [c for c in tablica]  # skopiuj tablice
        tablica_copy[krok], tablica_copy[i] = tablica_copy[i], tablica_copy[krok]  # zamien aktualny indeks z krokiem
        bruteforce(tablica_copy, wynik, krok + 1)  # rekurencja


def BF(tablica):
    wynik = []
    bruteforce(tablica, wynik)
    return wynik


def Cmax(tab, n, m):
    G = graf_rozwiazania(tab, n, m)
    C = copy.deepcopy(G)
    for item in C:
        for itemofitem in item:
            C[C.index(item)][C[C.index(item)].index(itemofitem)] = 0
    S = copy.deepcopy(C)            # C i S zerowe macierze o rozmiarach takich jak G
    for i in range(0, m):
        for j in range(0, n):
                S[i][j] = max(C[i][j - 1], C[i - 1][j])
                C[i][j] = S[i][j] + G[i][j]
    return C[m - 1][n - 1]


def zad1(files):
    for i in range(0, len(files)):
        dane = pobierz_dane(files[i])
        n = dane[0][0]
        m = dane[0][1]
        dane = dane[1:]
        for item in dane:
            dane[dane.index(item)] = item[1::2]
        print(files[i], Cmax(dane, n, m), "n=", n, "m=", m)
        kombinacje = BF(dane)
        wynik = []
        for item in kombinacje:
            wynik.append(Cmax(item, n, m))
        print("opt ", min(wynik))


if __name__ == "__main__":
    pliki = ["data001.txt", "data002.txt", "data003.txt", "data004.txt", "data005.txt", "data006.txt"]
    zad1(pliki)
