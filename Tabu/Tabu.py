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
    plik = "test_files/" + plik
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


def graf_rozwiazania(tab):
    g = []
    n = len(tab)
    m = len(tab[0]) - 1
    for i in range(0, m):
        g.append([])
        for j in range(0, n):
            g[i].append(tab[j][i])
    return g


def kolejnosc(lista):
    y = []
    m = len(lista[0]) - 1
    for item in lista:
        y.append(item[m])
    return y


def Cmax(tab):
    G = graf_rozwiazania(tab)
    n = len(tab)
    m = len(tab[0]) - 1
    C = np.zeros(shape=[len(G), len(G[0])])
    S = np.zeros(shape=[len(G), len(G[0])])  # C i S zerowe macierze o rozmiarach takich jak G
    for i in range(0, m):
        for j in range(0, n):
            S[i][j] = max(C[i][j - 1], C[i - 1][j])
            C[i][j] = S[i][j] + G[i][j]
    return [C[m - 1][n - 1], kolejnosc(tab)]


class Tabu:
    def __init__(self, plik, itLimit):
        self.itLimit = itLimit
        N = pobierz_dane(plik)
        self.pi = []
        self.n = N[0][0]
        self.m = N[0][1]
        N.remove(N[0])
        i = 0
        for item in N:
            self.pi.append(item[1::2])
            self.pi[self.pi.index(item[1::2])].append(i)
            i += 1
        self.TabuList = np.zeros(shape=[self.n, self.n])
        self.j_star = 0
        self.k_star = 0
        self.Cbest = 0
        self.pi_star = copy.deepcopy(self.pi)
        self.Search()
        print(Cmax(self.pi_star))

    def Search(self):
        for it in range(0, self.itLimit):
            self.Cbest = math.inf
            for j in range(0, self.n):
                for k in range(j+1, self.n):
                    if self.TabuList[j, k] < it:
                        pi_new = copy.deepcopy(self.pi)
                        pi_new[j], pi_new[k] = pi_new[k], pi_new[j]
                        if Cmax(pi_new)[0] < self.Cbest:
                            self.Cbest = Cmax(pi_new)[0]
                            self.j_star = j
                            self.k_star = k
            self.pi[self.j_star], self.pi[self.k_star] = self.pi[self.k_star], self.pi[self.j_star]
            self.TabuList[self.j_star, self.k_star] = it
            if Cmax(self.pi)[0] < Cmax(self.pi_star)[0]:
                self.pi_star = copy.deepcopy(self.pi)


if __name__ == "__main__":
    pliki = [f for f in listdir("test_files/") if isfile(join("test_files/", f))]
    file = open("Wyniki_Tabu_100_it.txt", "w")
    file.write("100 it\n")
    for item in pliki:
        start = time.time_ns()
        wynik = str(Cmax(Tabu(item, 100).pi_star))
        end = time.time_ns()
        n = (end - start) / 1000000
        decimals = 14 - len(str(int(n)))
        czas = '{:.{prec}f}'.format(n, prec=decimals)