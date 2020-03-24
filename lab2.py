import os


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
                # linia = linia.decode("utf-8")  # odczytujemy znaki jako utf-8
                # dodajemy elementy do tupli a tuplę do listy
                x = map(int, linia.split(" "))
                x = list(x)
                x.append(i)
                dane.append(tuple(x))
                i = i + 1
    else:
        print("Plik z danymi", plik, "nie istnieje!")
    return tuple(dane)  # przekształcamy listę na tuplę i zwracamy ją


def kolejnosc(lista):
    y = []
    for i in range(len(lista)):
        y.append(lista[i][3])
    return y


def calculate(tablica, n):
    #   S(0)=r_pi(0)
    S = [tablica[0][0]]
    #   C(0)=S_0 + p_pi(0)
    C = [S[0] + tablica[0][1]]
    #   C_max=C(0) + q_pi(0)
    Cmax = C[0] + tablica[0][2]
    for i in range(1, n):
        # S(i)=max(r_pi(i),c_i-1)
        S.append(max(tablica[i][0], C[i - 1]))
        # C(i)=S(i)+p_pi(i)
        C.append(S[i] + tablica[i][1])
        # C_max=max(C_max,C(i)+q_pi(i))
        Cmax = max(Cmax, C[i] + tablica[i][2])
    return Cmax


def Schrage(tablica, n):
    k = 0
    # G - zbiór zadań gotowych do realizacji
    G = []
    # N - zbiór zadań nieuszeregowanych
    N = list(tablica)
    # t - zmienna pomocnicza symbolizująca chwilę czasową
    # t = min(r_j) z N
    t = min(N, key=lambda x: x[0])[0]
    # wynik - pusta tablica o wielkości n
    wynik = [None] * n
    # while G nie pusty lub N nie pusty
    while len(G) != 0 or len(N) != 0:
        # while N nie pusty i min r_j z N mniejszy lub równy t
        while len(N) != 0 and t >= min(N, key=lambda x: x[0])[0]:
            # j = arg min r_j z N (minimum z N posortowane po r)
            j = min(N, key=lambda x: x[0])
            # G = G z j
            G.append(j)
            # N = N bez j
            N.remove(j)
        # jeżeli G nie pusty
        if len(G) != 0:
            # j = arg max q_j z G (maximum z G posortowane po q)
            j = max(G, key=lambda x: x[2])
            # G = G bez j
            G.remove(j)
            # wynik z indeksem k = j
            wynik[k] = j
            # t = t + p_j
            t = t + j[1]
            # k++
            k = k + 1
        else:
            # t = min r_j z N (minimum z N posortowane po r)
            t = min(N, key=lambda x: x[0])[0]
    return wynik


def SchragePmtn(tablica, n):
    Cmax = 0
    # G - zbiór zadań gotowych do realizacji
    G = []
    # N - zbiór zadań nieuszeregowanych
    N = list(tablica)
    # t - zmienna pomocnicza symbolizująca chwilę czasową
    t = 0
    l = [0,0,0,0]
    l[2]=100000000
    # while G nie pusty lub N nie pusty
    while len(G) != 0 or len(N) != 0:
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
        wynikalg = Schrage(dane, n)
        print("kolejnosc wyniku schrage: ", kolejnosc(wynikalg))
        print("Cmax=", calculate(wynikalg, n))
        print("Cmax SchragePmtn=", SchragePmtn(dane, n))


pliki = ["data10.txt", "data20.txt", "data50.txt", "data100.txt", "data200.txt", "data500.txt"]
lab2(pliki)

