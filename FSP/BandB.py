import fsp_1
import math
import copy
import numpy as np

def LowerBound1(tab, x):
    G = np.array(fsp_1.graf_rozwiazania(tab, len(tab), len(tab[0]) - 1))
    wynik = []
    C = np.zeros(shape=[len(G),len(G[0])])
    S = np.zeros(shape=[len(G),len(G[0])])
    for i in range(0, len(tab[0]) - 1):
        pom = 0
        for j in range(0, len(tab)):
            S[i][j] = max(C[i][j - 1], C[i - 1][j])
            C[i][j] = S[i][j] + G[i][j]
            if j > x:
                pom += G[i][j]
        wynik.append(C[i][x]+pom)
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
        LB = LowerBound1(pi, len(pi)-1)
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
        dane = fsp_1.pobierz_dane(file)
        n = dane[0][0]
        m = dane[0][1]
        dane = dane[1:]
        dane = fsp_1.przeksztalc(dane)
        print(fsp_1.Cmax(BnB(dane), n, m))


if __name__ == "__main__":
    #dane = fsp_1.pobierz_dane("data001.txt")
    #n = dane[0][0]
    #m = dane[0][1]
    #dane = dane[1:]
    #dane = fsp_1.przeksztalc(dane)
    #print(fsp_1.Cmax(BnB(dane), n, m))
    pliki = ("data000.txt", "data001.txt", "data002.txt", "data003.txt", "data004.txt", "data005.txt", "data006.txt")
    zad3(pliki[0])
