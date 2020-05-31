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


def kolejnosc(lista):
    y = []
    m = len(lista[0]) - 1
    for item in lista:
        y.append(item[m])
    return y


def graf_rozwiazania(tab):
    g = []
    n = len(tab)
    m = len(tab[0]) - 1
    for i in range(0, m):
        g.append([])
        for j in range(0, n):
            g[i].append(tab[j][i])
    return g


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


def Cmax_naturalnych(files):
    for i in range(0, len(files)):
        dane = pobierz_dane(files[i])
        n = dane[0][0]
        m = dane[0][1]
        dane = dane[1:]
        j = 0
        for item in dane:
            print(item[1::2])
            dane[dane.index(item)] = item[1::2]
            dane[dane.index(item[1::2])].append(j)
            j = j + 1
        print(files[i], Cmax(dane), "n=", n, "m=", m)


class Node:
    """Klasa modelująca zadanie"""

    def __init__(self, zadanie):
        self.p = zadanie[1::2]

    def __repr__(self):
        return "<c:%s>" % (self.p)

    def __str__(self):
        return "%s" % (self.p)


class SAA:
    """Klasa realizująca algorytm symulowanego wyżarzania"""

    def __init__(self, plik, metoda):
        N = pobierz_dane(plik)
        self.pi = []
        self.n = N[0][0]
        self.m = N[0][1]
        self.metoda = metoda
        N.remove(N[0])
        i = 0
        for item in N:
            # self.pi.append([Node(item), i])
            self.pi.append(item[1::2])
            self.pi[self.pi.index(item[1::2])].append(i)
            i += 1
        self.cmax = Cmax(self.pi)
        self.pi_star = self.pi
        self.cmax_star = Cmax(self.pi_star)
        self.T = 0
        self.alfa = 0.90  # tu wpisujemy wartość alfa
        self.saa(10 ** 2, 10, self.n)  # tu wpisujemy z jakimi parametrami uruchomić algorytm
        # T0, Tend, L
        print(plik, self.cmax_star)

    def saa(self, T0, Tend, L):
        x = T0 / (10 ** 3)  # tu wpisujemy metode liczenia x
        self.T = T0
        while self.T > Tend:
            for k in range(1, int(L)):
                pi_new = copy.deepcopy(self.pi)
                i = random.randint(0, self.n - 1)
                if self.metoda == "adj":
                    if i < self.n - 1:
                        pi_new[i], pi_new[i + 1] = pi_new[i + 1], pi_new[i]
                    else:
                        pi_new[i], pi_new[i - 1] = pi_new[i - 1], pi_new[i]
                else:
                    j = random.randint(0, self.n - 1)
                    pi_new[i], pi_new[j] = pi_new[j], pi_new[i]
                new_cmax = Cmax(pi_new)
                # print("pi",self.pi,"pi_new", pi_new, i)
                if new_cmax[0] > self.cmax[0]:
                    r = random.random()
                    if r >= math.e ** ((self.cmax[0] - new_cmax[0]) / self.T):
                        pi_new = self.pi
                        new_cmax = self.cmax
                self.pi = pi_new
                self.cmax = new_cmax
                if self.cmax[0] < self.cmax_star[0]:
                    self.pi_star = copy.deepcopy(self.pi)
                    self.cmax_star = copy.deepcopy(self.cmax)
            self.T -= x                 # tu wybieramy schemat chlodzenia
            #self.T = self.T * self.alfa

    def SAA_cmax_star(self):
        return self.cmax_star


if __name__ == "__main__":
    pliki = ["test_files/ta001.txt",
             "test_files/ta002.txt"]  # , "data000.txt", "data001.txt", "data002.txt", "data003.txt", "data004.txt", "data005.txt", "data006.txt"]
    pliki = [f for f in listdir("test_files/") if isfile(join("test_files/", f))]
    # Open function to open the file "MyFile1.txt"
    # (same directory) in read mode and
    file = open("Wyniki_10_2_n_T0_10_-3.txt", "w")
    file.write("adj\n")
    #for item in pliki:
    #    start = time.time_ns()
    #    wynik = str(SAA(item, "adj").cmax_star)
    #    end = time.time_ns()
    #    n = (end - start) / 1000000
    #    decimals = 14 - len(str(int(n)))
    #    czas = '{:.{prec}f}'.format(n, prec=decimals)
    #    file.write(item + ", time:" + czas + ", odp:" + wynik + "\n")
    for i in range(0, 10):
        start = time.time_ns()
        wynik = str(SAA(pliki[i], "adj").cmax_star)
        end = time.time_ns()
        n = (end - start) / 1000000
        decimals = 14 - len(str(int(n)))
        czas = '{:.{prec}f}'.format(n, prec=decimals)
        file.write(pliki[i] + ", time:" + czas + ", odp:" + wynik + "\n")
        print(pliki[i] + ", time:" + czas + ", odp:" + wynik + "\n")
    i = 0
    while i < 120:
        start = time.time_ns()
        wynik = str(SAA(pliki[i], "adj").cmax_star)
        end = time.time_ns()
        n = (end - start) / 1000000
        decimals = 14 - len(str(int(n)))
        czas = '{:.{prec}f}'.format(n, prec=decimals)
        file.write(pliki[i] + ", time:" + czas + ", odp:" + wynik + "\n")
        print(pliki[i] + ", time:" + czas + ", odp:" + wynik + "\n")
        i+=10
    file.write("swap\n")
    #for item in pliki:
    #    start = time.time_ns()
    #    wynik = str(SAA(item, "swap").cmax_star)
    #    end = time.time_ns()
    #    n = (end - start) / 1000000
    #    decimals = 14 - len(str(int(n)))
    #    czas = '{:.{prec}f}'.format(n, prec=decimals)
    #    file.write(item + ", time:" + czas + ", odp:" + wynik + "\n")
    for i in range(0, 10):
        start = time.time_ns()
        wynik = str(SAA(pliki[i], "swap").cmax_star)
        end = time.time_ns()
        n = (end - start) / 1000000
        decimals = 14 - len(str(int(n)))
        czas = '{:.{prec}f}'.format(n, prec=decimals)
        file.write(pliki[i] + ", time:" + czas + ", odp:" + wynik + "\n")
        print(pliki[i] + ", time:" + czas + ", odp:" + wynik + "\n")
    i = 0
    while i < 120:
        start = time.time_ns()
        wynik = str(SAA(pliki[i], "swap").cmax_star)
        end = time.time_ns()
        n = (end - start) / 1000000
        decimals = 14 - len(str(int(n)))
        czas = '{:.{prec}f}'.format(n, prec=decimals)
        file.write(pliki[i] + ", time:" + czas + ", odp:" + wynik + "\n")
        print(pliki[i] + ", time:" + czas + ", odp:" + wynik + "\n")
        i+=10