import fsp_1
import math
import copy
import numpy as np

def Bound(tab, x):
    G = np.array(fsp_1.graf_rozwiazania(tab, len(tab), len(tab[0]) - 1))
    wynik = []
    C = np.zeros(shape=[len(G),len(G[0])])
    S = np.zeros(shape=[len(G),len(G[0])])
    for i in range(0, len(tab[0]) - 1):
        pom = 0
        for j in range(0, len(tab)):
            S[i][j] = max(C[i][j - 1], C[i - 1][j])
            C[i][j] = S[i][j] + G[i][j]
            pom += G[i][j]
        wynik.append(C[i][x]+pom)
    return max(wynik)


def BNB(j_star, N, pi, UB, pi_star, J):
    pi.append(j_star)
    N.remove(j_star)
    if N:
        LB = Bound(J, len(pi)-1)
        if LB <= UB[0]:
            for i in N:
                BNB(i, N, pi, UB, pi_star, J)
    else:
        Cmax = fsp_1.Cmax(pi, len(pi), len(pi[0]) - 1)
        if Cmax[0] < UB[0]:
            UB[0] = Cmax[0]
            pi_star[0] = copy.deepcopy(pi)


def BnB(J):
    pi_star = [0]
    pi = []
    N = copy.deepcopy(J)
    UB = [math.inf]

    for j in N:
        BNB(j, N, pi, UB, pi_star, J)
    return pi_star[0]


if __name__ == "__main__":
    dane = fsp_1.pobierz_dane("data000.txt")
    n = dane[0][0]
    m = dane[0][1]
    dane = dane[1:]
    dane = fsp_1.przeksztalc(dane)
    print(fsp_1.Cmax(BnB(dane), n, m))
    #fsp_1.zad1(["data001.txt"])
