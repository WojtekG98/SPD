import fsp_1
import math
import copy


def BnB(J):
    pi_star = [0]
    pi = []
    N = copy.deepcopy(J)
    UB = [math.inf]

    def Bound(tab):
        G = fsp_1.graf_rozwiazania(tab, len(tab), len(tab[0]) - 1)
        return 443

    def BNB(j_star, N_2, pi_2, UB):
        pi_2.append(j_star)
        N_2.remove(j_star)
        if N_2:
            LB = Bound(pi_2)
            if LB <= UB[0]:
                for i in N_2:
                    BNB(i, N_2, pi_2, UB)
        else:
            Cmax = fsp_1.Cmax(pi_2, len(pi_2), len(pi_2[0]) - 1)
            if Cmax[0] < UB[0]:
                UB[0] = Cmax
                pi_star[0] = copy.deepcopy(pi_2)


    for j in N:
        BNB(j, N, pi, UB)
    return pi_star[0]


if __name__ == "__main__":
    dane = fsp_1.pobierz_dane("data001.txt")
    n = dane[0][0]
    m = dane[0][1]
    dane = dane[1:]
    dane = fsp_1.przeksztalc(dane)
    print(n, m, dane)
    print(BnB(dane))
