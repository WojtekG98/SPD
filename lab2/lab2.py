import os
import time
import heapq
import math
import copy
def pobierz_dane(plik):
    """
    Funkcja zwraca tuplę tupli zawierających dane pobrane z pliku csv
    do zapisania w tabeli.
    """
    dane = []  # deklarujemy pustą listę
    if os.path.isfile(plik):  # sprawdzamy czy plik istnieje na dysku
        with open(plik, "r") as zawartosc:  # otwieramy plik do odczytu
            i = 0
            for linia in zawartosc:
                linia = linia.replace("\n", "")  # usuwamy znaki końca linii
                linia = linia.replace("\r", "")  # usuwamy znaki końca linii
                x = map(int, linia.split(" "))   # dodajemy elementy do tupli a tuplę do listy
                x = list(x)                      # tutaj takie wygibasy żeby dodać czwarta liczbę
                x.append(i)                      # która jest kolejnością zadań
                dane.append(list(x))            # pewnie da się ładniej ale jestem nowy w Python
                i = i + 1                        # i++ zadania są numerowane od 1 do n
    else:
        print("Plik z danymi", plik, "nie istnieje!")
    return list(dane)  # przekształcamy listę na tuplę i zwracamy ją


def kolejnosc(lista):
    y = []
    for item in lista:
        y.append(item[3])
    return y


def calculate(tablica, n):
    S = [tablica[0][0]]                           #   S(0)=r_pi(0)
    C = [S[0] + tablica[0][1]]                    #   C(0)=S_0 + p_pi(0)
    Cmax = C[0] + tablica[0][2]                   #   C_max=C(0) + q_pi(0)
    for i in range(1, n):                         # for i = 1,2,3,...,n-1
        S.append(max(tablica[i][0], C[i - 1]))    # S(i)=max(r_pi(i),c_i-1)
        C.append(S[i] + tablica[i][1])            # C(i)=S(i)+p_pi(i)
        Cmax = max(Cmax, C[i] + tablica[i][2])    # C_max=max(C_max,C(i)+q_pi(i))
    return Cmax

def Schrage(tablica, n):
    k = 0
    G = []                                        # G - zbiór zadań gotowych do realizacji
    N = list(tablica)                             # N - zbiór zadań nieuszeregowanych
    t = min(N, key=lambda x: x[0])[0]             # t - zmienna pomocnicza symbolizująca chwilę czasową t = min(r_j) z N
    wynik = [None] * n                            # wynik - pusta tablica o wielkości n
    while len(G) != 0 or len(N) != 0:             # while G nie pusty lub N nie pusty
                                                  # while N nie pusty i min r_j z N mniejszy lub równy t
        while len(N) != 0 and t >= min(N, key=lambda x: x[0])[0]:
            j = min(N, key=lambda x: x[0])        # j = arg min r_j z N (minimum z N posortowane po r)
            G.append(j)                           # G = G z j
            N.remove(j)                           # N = N bez j
        if len(G) != 0:                           # jeżeli G nie pusty
            j = max(G, key=lambda x: x[2])        # j = arg max q_j z G (maximum z G posortowane po q)
            G.remove(j)                           # G = G bez j
            wynik[k] = j                          # wynik z indeksem k = j
            t = t + j[1]                          # t = t + p_j
            k = k + 1                             # k++
        else:
            t = min(N, key=lambda x: x[0])[0]     # t = min r_j z N (minimum z N posortowane po r)
    return wynik

def Schrage_queue(tablica, n):
    k = 0
    G = []                                        # G - zbiór zadań gotowych do realizacji
    heap_N = list(tablica)                        # heap_N - zbiór zadań nieuszeregowanych
    heapq.heapify(heap_N)                         # zrob z tablicy heap w czasie liniowym
    t = heap_N[0][0]                              # t - zmienna pomocnicza symbolizująca chwilę czasową t = min(r_j) z N
    wynik = [None] * n                            # wynik - pusta tablica o wielkości n
    while len(G) != 0 or len(heap_N) != 0:             # while G nie pusty lub N nie pusty
        while len(heap_N) != 0 and t >= heap_N[0][0]:       # while heap_N nie pusty i min r_j z N mniejszy lub równy t
            j = heapq.heappop(heap_N)             # j = arg min r_j z heap_N
            rj=j[0]                               # takie bajery zeby sortowalo po q i rosnaco
            qj=j[2]
            j=list(j)
            j[0]=-qj
            j[2]=rj
            heapq.heappush(G,j)                   # G = G z j
        if len(G) != 0:                           # jeżeli G nie pusty
            j = heapq.heappop(G)                  # j = arg max q_j z G
            qj=j[0]                               # takie bajery zeby sortowalo po q i rosnaco
            rj=j[2]
            j=list(j)
            j[0]=rj
            j[2]=-qj
            wynik[k] = j                          # wynik z indeksem k = j
            t = t + j[1]                          # t = t + p_j
            k = k + 1                             # k++
        else:
            t = heap_N[0][0]                          # t = min r_j z N (minimum z N posortowane po r)
    return wynik

def SchragePmtn(tablica, n):
    Cmax = 0                                      # Cmax = 0
    G = []                                        # G - zbiór zadań gotowych do realizacji
    N = list(tablica)                             # N - zbiór zadań nieuszeregowanych
    t = 0                                         # t - zmienna pomocnicza symbolizująca chwilę czasową
    l = [0,0,0,0]                                 # l = 0
    l[2]=100000000                                # q0 = nieskonczonosc
    while len(G) != 0 or len(N) != 0:             # while G nie pusty lub N nie pusty
                                                  # while N nie pusty i min r_j z N mniejszy lub równy t
        while len(N) != 0 and t >= min(N, key=lambda x: x[0])[0]:
            j = min(N, key=lambda x: x[0])        # j = arg min r_j z N (minimum z N posortowane po r)
            G.append(j)                           # G = G z j
            N.remove(j)                           # N = N bez j
            if j[2] > l[2]:                       # jeżeli q_j większe od q_wynik z indeksem l-1
                l=list(l)                         # p_l-1 = t - r_j
                l[1] = t - j[0]
                t = j[0]                          # t = r_j
                if l[1] > 0:                      # jeżeli p_l-1 > 0
                    G.append(l)                   # G = G z j
        if len(G) != 0:                           # jeżeli G nie pusty
            j = max(G, key=lambda x: x[2])        # j = arg max q_j z G (maximum z G posortowane po q)
            G.remove(j)                           # G = G bez j
            l=j                                   # l = j
            t = t + j[1]                          # t = t + p_j
            Cmax = max(Cmax, t + j[2])            # Cmax = max(Cmax,t+q_j)
        else:                                     # jeżeli G pusty
            t = min(N, key=lambda x: x[0])[0]     # t = min r_j z N (minimum z N posortowane po r)
    return Cmax

def SchragePmtn_queue(tablica, n):
    Cmax = 0                                      # Cmax = 0
    G = []                                        # G - zbiór zadań gotowych do realizacji
    N = list(tablica)                             # N - zbiór zadań nieuszeregowanych
    heapq.heapify(N)
    t = 0                                         # t - zmienna pomocnicza symbolizująca chwilę czasową
    l = [0,0,0,0]                                 # l = 0
    l[2]=100000000                                # q0 = nieskonczonosc
    while len(G) != 0 or len(N) != 0:             # while G nie pusty lub N nie pusty
                                                  # while N nie pusty i min r_j z N mniejszy lub równy t
        while len(N) != 0 and t >= N[0][0]:
            j = heapq.heappop(N)                  # j = arg min r_j z N (minimum z N posortowane po r) i N = N bez j
            rj=j[0]                               # takie bajery zeby sortowalo po q i rosnaco
            qj=j[2]
            j=list(j)
            j[0]=-qj
            j[2]=rj
            heapq.heappush(G,j)                   # G = G z j
            if qj > l[2]:                         # jeżeli q_j większe od q_l
                l=list(l)                         # p_l-1 = t - r_j
                l[1] = t - rj
                t = rj                            # t = r_j
                if l[1] > 0:                      # jeżeli p_l-1 > 0
                    rl=l[0]                       # takie bajery zeby sortowalo po q i rosnaco
                    ql=l[2]
                    l[0]=-ql
                    l[2]=rl
                    heapq.heappush(G, l)          # G = G z l
        if len(G) != 0:                           # jeżeli G nie pusty
            j = heapq.heappop(G)                  # j = arg max q_j z G i  G = G bez j
            qj=j[0]                               # takie bajery zeby sortowalo po q i rosnaco
            rj=j[2]
            j=list(j)
            j[0]=rj
            j[2]=-qj
            l=j                                   # l = j
            t = t + j[1]                          # t = t + p_j
            Cmax = max(Cmax, t + j[2])            # Cmax = max(Cmax,t+q_j)
        else:                                     # jeżeli G pusty
            t = N[0][0]                           # t = min r_j z N (minimum z N posortowane po r)
    return Cmax

def Carlier(tablica, n):                            # funkcja wywolujaca funkcje bo inaczej
                                                    # nie dzialalo przekazywanie UB przez referencje
    UB = [math.inf]                                 # UB = inf
    do_Carlier(tablica, UB)                         # wykonaj Carliera
    return UB[0]                                    # zwroc wynik

def do_Carlier(tablica, UB):
    Pi = Schrage(tablica, len(tablica))
    U = calculate(Pi,len(Pi))                       # U <- Schrage(J)
    if U < UB[0]:                                   # jeżeli U   UB, a UB[0] bo chcemy udawana referencje mieć
        UB[0]=U                                     # UB = U
    b, c = znajdz_b_c(Pi)                           # a jest potrzebne tylko do szukania c
    if c is None:                                   # jeżeli c puste to return
        return
    K = znajdz_k(Pi, c, b)                          # K = Pi[c,b]
    r = min(K, key=lambda x: x[0])[0]               # r = min r z K
    q = min(K, key=lambda x: x[2])[2]               # q = min q z K
    p = 0
    for item in K:
        p = p + item[1]                             # p = sum p_i, i z K
    r_tmp = c[0]
    c[0]=max(r_tmp, r + p)                          # r_pi = max(r_pi, r+p)
    LB = SchragePmtn(Pi,len(Pi))                    # LB = SchragePmtn(Pi)
    if LB < UB[0]:                                  # jeżeli U   UB, a UB[0] bo chcemy udawana referencje mieć
        do_Carlier(Pi, UB)                          # rekurencja
    c[0]=r_tmp                                      # restore r_pi(c)
    q_tmp = c[2]
    c[2]= max(q_tmp, q + p)                          # q_pi = max (q_pi, q + p)
    LB = SchragePmtn(Pi,len(Pi))
    if LB < UB[0]:                                  # jeżeli U   UB, a UB[0] bo chcemy udawana referencje mieć
        do_Carlier(Pi,UB)                           # rekurencja
    c[2] = q_tmp                                    # restore q_pi(c)

def znajdz_b_c(Pi):
        t = 0
        Cmax = calculate(Pi,len(Pi))
        b = None
        for zadanie in Pi:
            t = max(t, zadanie[0]) + zadanie[1]
            if t + zadanie[2] == Cmax:
                b = zadanie
        a = None
        p = 0
        for zadanie in Pi:
            p = p + zadanie[1]
            if zadanie == b:
                break

        for zadanie in Pi:
            if Cmax == zadanie[0] + p + b[2]:
                a = zadanie
                break
            p = p - zadanie[1]
            if zadanie == b:
                break

        c = None
        for zadanie_index in range(Pi.index(a), Pi.index(b)):
            if b[2] > Pi[zadanie_index][2]:
                c = Pi[zadanie_index]
        return b, c

def znajdz_k(Pi, c, b):
        k = []
        czy_dodac = False
        for zadanie in Pi:
            if czy_dodac:
                k.append(zadanie)
            if c == zadanie:
                czy_dodac = True
            if zadanie == b:
                break
        return k

def lab1(pliki):
    for j in range(0, 6):
        dane = pobierz_dane(pliki[j])
        n = dane[0][0]
        r = dane[0][1]
        dane = list(dane[1:n + 1])
        wynik = calculate(dane, n)
        print("Nazwa pliku: ", pliki[j])
        print("Wynik nieposortowany:", wynik)
        print(kolejnosc(dane))
        dane.sort(key=lambda x: x[0])
        wynik = calculate(dane, n)
        print("Wynik posortowany:", wynik)
        print(kolejnosc(dane))


def lab2(pliki):
    for j in range(0, len(pliki)):
        dane = pobierz_dane(pliki[j])
        n = dane[0][0]
        r = dane[0][1]
        dane = list(dane[1:n + 1])
        dane = tuple(dane)
        start_queue = time.time_ns()
        wynikalg_queue = Schrage_queue(dane, n)
        Cmax_queue=calculate(wynikalg_queue,n)
        end_queue = time.time_ns()
        start = time.time_ns()
        wynikalg = Schrage(dane,n)
        Cmax=calculate(wynikalg,n)
        end = time.time_ns()
        print("\nNazwa pliku: ", pliki[j])
        print("Schrage Cmax=", Cmax,", w czasie:",(end-start)/1000000," ms")
        print("Schrage_queue Cmax=", Cmax_queue,", w czasie:",(end_queue-start_queue)/1000000," ms")
        start=time.time_ns()
        Cmax=SchragePmtn(dane, n)
        end=time.time_ns()
        print("Cmax SchragePmtn=", Cmax,", w czasie:",(end-start)/1000000," ms")
        start=time.time_ns()
        Cmax=SchragePmtn_queue(dane, n)
        end=time.time_ns()
        print("Cmax SchragePmtn_queue=", Cmax,", w czasie:",(end-start)/1000000," ms")

def lab3(pliki):
    for i in range(0, len(pliki)):
        dane = pobierz_dane(pliki[i])
        n = dane[0][0]
        r = dane[0][1]
        dane = (dane[1:n + 1])
        odp = Carlier(dane, n)
        print(odp)

pliki = ["data10.txt", "data20.txt", "data50.txt", "data100.txt", "data200.txt", "data500.txt"]
#lab1(pliki)
#lab2(pliki)
lab3(pliki)