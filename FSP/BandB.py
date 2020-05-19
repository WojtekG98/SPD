import fsp_1
import math
import copy
import numpy as np

def LowerBound1(tab, N):
    G = np.array(fsp_1.graf_rozwiazania(tab + N, len(tab) + len(N), len(tab[0]) - 1))
    #print('len(tab)', len(tab))
    #print('tab', tab)
    #print('N', N)
    #print('G:', G)
    wynik = []
    C = np.zeros(shape=[len(G), len(G[0])])
    S = np.zeros(shape=[len(G), len(G[0])])
    for i in range(0, len(tab[0]) - 1):
        for j in range(0, len(tab + N)):
            S[i][j] = max(C[i][j - 1], C[i - 1][j])
            C[i][j] = S[i][j] + G[i][j]
    for i in range(0, len(C)):
        wynik.append(C[i][len(tab)-1] + sum(G[i][len(tab):]))
    #print(wynik)

    #i = 0
    #for item in G_N:
    #    wynik.append(C[i][len(tab) - 1] + sum(item))
    #    i += 1
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
        LB = LowerBound1(copy.deepcopy(pi), copy.deepcopy(N))
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
        odp = BnB(dane)
        #print(odp)
        print(fsp_1.Cmax(odp, n, m))


if __name__ == "__main__":
    pliki = ("data000.txt", "data001.txt", "data002.txt", "data003.txt", "data004.txt", "data005.txt", "data006.txt")
    zad3(pliki)
