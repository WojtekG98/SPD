import os
import math
import itertools


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



def calculate(tablica,n):
    S=0
    C=tablica[0][0]
    T=max(C-tablica[0][2],0)
    F=tablica[0][1]*T

    for i in range (1,n):
        S = C
        C = S + tablica[i][0]
        T = max(C - tablica[i][2],0)
        K = T*tablica[i][1]
        F = F + K

    return F

def bruteforce(tablica, wynik, krok = 0):
    if krok == len(tablica):
        wynik.append(tablica)                                                       # koniec, dodaj permutacje
    for i in range(krok, len(tablica)):
        tablica_copy = [c for c in tablica]                                         # skopiuj tablice
        tablica_copy[krok], tablica_copy[i] = tablica_copy[i], tablica_copy[krok]   # zamien aktualny indeks z krokiem
        bruteforce(tablica_copy, wynik, krok + 1)                                   # rekurencja

def BF(tablica):
    wynik = []
    bruteforce(tablica, wynik)
    return wynik

def permut(tablica, n):
    #wynik = list(itertools.permutations(tablica))
    wynik = BF(tablica)
    P = 100000
    for i in range(0, math.factorial(n)):
        kolej = wynik[i]
        K = calculate(kolej, n)
        P = min(P, K)

    return P


def zad1(pliki):
    for j in range(0, len(pliki)):
        dane = pobierz_dane(pliki[j])
        n = dane[0][0]
        r = dane[0][1]
        dane = list(dane[1:n + 1])
        wynik = calculate(dane, n)
        print("Nazwa pliku: ", pliki[j])
        print("Wynik nieposortowany:", wynik)
        #print(kolejnosc(dane))
        dane.sort(key=lambda x: x[2])
        wynik = calculate(dane, n)
        print("Wynik posortowany:", wynik)
        print("---")
        print(kolejnosc(dane))
        print("---")


def zad2(pliki):
    for i in range(0, len(pliki)):
        dane = pobierz_dane(pliki[i])
        n = dane[0][0]
        r = dane[0][1]
        dane = list(dane[1:n + 1])
        wynik = permut(dane, n)
        print("Nazwa pliku: ", pliki[i])
        print("Wynik: ", wynik)


pliki = ["data10.txt", "data11.txt", "data12.txt", "data13.txt", "data14.txt", "data15.txt", "data16.txt", "data17.txt", "data18.txt", "data19.txt", "data20.txt"]
zad2(pliki)