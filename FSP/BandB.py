import fsp_1
import math
import copy
import time
import numpy as np

def LowerBound1(tab, N):
    G = np.array(fsp_1.graf_rozwiazania(tab + N, len(tab) + len(N), len(tab[0]) - 1))
    wynik = []
    C = np.zeros(shape=[len(G), len(G[0])])
    S = np.zeros(shape=[len(G), len(G[0])])
    for i in range(0, len(tab[0]) - 1):
        for j in range(0, len(tab + N)):
            S[i][j] = max(C[i][j - 1], C[i - 1][j])
            C[i][j] = S[i][j] + G[i][j]
    for i in range(0, len(C)):
        wynik.append(C[i][len(tab)-1] + sum(G[i][len(tab):]))
    return max(wynik)


def LowerBound2(tab, N):
    G = np.array(fsp_1.graf_rozwiazania(tab + N, len(tab) + len(N), len(tab[0]) - 1))
    wynik = []
    C = np.zeros(shape=[len(G), len(G[0])])
    S = np.zeros(shape=[len(G), len(G[0])])
    for i in range(0, len(tab[0]) - 1):
        for j in range(0, len(tab + N)):
            S[i][j] = max(C[i][j - 1], C[i - 1][j])
            C[i][j] = S[i][j] + G[i][j]
    for i in range(0, len(C)):
        pom = 0
        for k in range(i+1, len(C)):
            pom += min(G[k])
        wynik.append(C[i][len(tab) - 1] + sum(G[i][len(tab):]) + pom)
    return max(wynik)


def LowerBound3(tab, N):
    G = np.array(fsp_1.graf_rozwiazania(tab + N, len(tab) + len(N), len(tab[0]) - 1))
    wynik = []
    C = np.zeros(shape=[len(G), len(G[0])])
    S = np.zeros(shape=[len(G), len(G[0])])
    for i in range(0, len(tab[0]) - 1):
        for j in range(0, len(tab + N)):
            S[i][j] = max(C[i][j - 1], C[i - 1][j])
            C[i][j] = S[i][j] + G[i][j]
    for i in range(0, len(C)):
        pom = 0
        for k in range(i+1, len(C)):
            pom += min(G[k][len(tab):])
        wynik.append(C[i][len(tab) - 1] + sum(G[i][len(tab):]) + pom)
    return max(wynik)


def LowerBound4(tab, N):
    G = np.array(fsp_1.graf_rozwiazania(tab + N, len(tab) + len(N), len(tab[0]) - 1))
    wynik = []
    C = np.zeros(shape=[len(G), len(G[0])])
    S = np.zeros(shape=[len(G), len(G[0])])
    for i in range(0, len(tab[0]) - 1):
        for j in range(0, len(tab + N)):
            S[i][j] = max(C[i][j - 1], C[i - 1][j])
            C[i][j] = S[i][j] + G[i][j]
    for i in range(0, len(C)):
        pom = []
        for k in range(i+1, len(C)):
            print(i, k ,len(C))
            print(G[k])
            print(G[k][len(tab):])
            print(sum(G[k][len(tab):]))
            pom.append(sum(G[k][len(tab):]))
        if len(pom) != 0:
            print(min(pom))
            print(C[i][len(tab) - 1] + sum(G[i][len(tab):]))
            print(fsp_1.Cmax(tab+N, len(tab + N), len(tab[0])-1))
            wynik.append(C[i][len(tab) - 1] + sum(G[i][len(tab):]) + min(pom))
        else:
            wynik.append(C[i][len(tab) - 1] + sum(G[i][len(tab):]))
    return max(wynik)


LB = 0
pi_star = [0]
UB = math.inf

def BNB(j, N, pi):
    global LB
    global pi_star
    global UB
    pi.append(j)
    N.remove(j)
    if N:
        # tu wybieramy która wersją LB liczymy
        LB = LowerBound4(copy.deepcopy(pi), copy.deepcopy(N))
        if LB <= UB:
            for j in N:
                BNB(j, copy.deepcopy(N), copy.deepcopy(pi))
    else:
        Cmax = fsp_1.Cmax(pi, len(pi), len(pi[0]) - 1)
        if Cmax[0] < UB:
            UB = Cmax[0]
            pi_star[0] = copy.deepcopy(pi)


def BnB(J):
    pi = []
    N = copy.deepcopy(J)

    for j in N:
        BNB(j, copy.deepcopy(N), copy.deepcopy(pi))
    return pi_star[0]


def zad3(file):
    for numer_pliku in range(0, len(file)):
        global LB
        global pi_star
        global UB
        LB = 0
        pi_star = [0]
        UB = math.inf
        dane = fsp_1.pobierz_dane(file[numer_pliku])
        n = dane[0][0]
        m = dane[0][1]
        print(n, m, numer_pliku)
        dane.remove(dane[0])
        j = 0
        for item in dane:
            dane[dane.index(item)] = item[1::2]
            dane[dane.index(item[1::2])].append(j)
            j = j + 1
        # tu wybieramy która wersja UB czy bardzo duża liczba czy Cmax naturalnej
        UB = math.inf
        # UB = fsp_1.Cmax(dane, n, m)[0]
        start = time.time_ns()
        odp = BnB(dane)
        end = time.time_ns()
        file1 = open("MyFile.txt", "w")
        string = "czas:", str((end-start)/1000000), "ms, cmax:", str(fsp_1.Cmax(odp, n, m)[0])
        print('czas:', (end-start)/1000000, "ms, cmax:", fsp_1.Cmax(odp, n, m))
        file1.write(''.join(string))
        file1.close()


if __name__ == "__main__":
    pliki = ("data000.txt", "data001.txt", "data002.txt", "data003.txt", "data004.txt", "data005.txt", "data006.txt")
    zad3(pliki)
