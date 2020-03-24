import os
import time

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
                dane.append(tuple(x))            # pewnie da się ładniej ale jestem nowy w Python
                i = i + 1                        # i++ zadania są numerowane od 1 do n
    else:
        print("Plik z danymi", plik, "nie istnieje!")
    return tuple(dane)  # przekształcamy listę na tuplę i zwracamy ją


def kolejnosc(lista):
    y = []
    for i in range(len(lista)):
        y.append(lista[i][3])
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
    N = list(tablica)                             # N - zbiór zadań nieuszeregowanych
    N.sort(reverse = True,key = lambda x: x[0])   # sortujemy rosnąco, bo pop() wyciąga ostatnia wartość
    t = N[len(N)-1][0]                            # t - zmienna pomocnicza symbolizująca chwilę czasową t = min(r_j) z N
    wynik = [None] * n                            # wynik - pusta tablica o wielkości n
    while len(G) != 0 or len(N) != 0:             # while G nie pusty lub N nie pusty
        while len(N) != 0 and t >= N[0][0]:       # while N nie pusty i min r_j z N mniejszy lub równy t
            j = N.pop()                           # j = arg min r_j z N (minimum z N posortowane po r)
            G.append(j)                           # G = G z j
            G.sort(key = lambda x: x[2])          # sortujemy malejąco, bo pop() wyciąga ostatnią wartość
        if len(G) != 0:                           # jeżeli G nie pusty
            j = G.pop()                           # j = arg max q_j z G (maximum z G posortowane po q)
            wynik[k] = j                          # wynik z indeksem k = j
            t = t + j[1]                          # t = t + p_j
            k = k + 1                             # k++
        else:
            t = N[0][0]                           # t = min r_j z N (minimum z N posortowane po r)
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

def Carlier(tablica, n):
    UB=1000000
    wynik=list(tablica)
    U = Schrage(tablica, n)
    if U < UB:
        UB=calculate(U,n)
        wynik_optymalny = U
    #a=
    #b=
    c=0
    if len(c)==0:
        return wynik_optymalny


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
    for j in range(0, 6):
        dane = pobierz_dane(pliki[j])
        n = dane[0][0]
        r = dane[0][1]
        dane = list(dane[1:n + 1])
        dane = tuple(dane)
        start_queue = time.time()
        wynikalg_queue = Schrage_queue(dane, n)
        end_queue = time.time()
        start = time.time()
        wynikalg = Schrage(dane,n)
        end = time.time()
        print("Czas Schrage:",end-start)
        print("Czas Schrage_queue",end_queue-start_queue)
        print("Nazwa pliku: ", pliki[j])
        print("kolejnosc wyniku Schrage: ", kolejnosc(wynikalg))
        print("Cmax=", calculate(wynikalg, n))
        print("kolejnosc wyniku Schrage_queue: ", kolejnosc(wynikalg_queue))
        print("Cmax=", calculate(wynikalg, n))
        print("Cmax SchragePmtn=", SchragePmtn(dane, n))


pliki = ["data10.txt", "data20.txt", "data50.txt", "data100.txt", "data200.txt", "data500.txt"]
lab2(pliki)

