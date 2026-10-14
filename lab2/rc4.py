from itertools import product
import string
import math
from time import perf_counter

def rc4(dane: bytes, klucz: bytes) -> bytes:
    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + klucz[i % len(klucz)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    rezultat = bytearray()

    for bajt in dane:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        K = S[(S[i] + S[j]) % 256]
        rezultat.append(bajt ^ K)

    return bytes(rezultat)


def entropia(dane: bytes):
    N = len(dane)
    histogram = [0] * 256

    for bajt in dane:
        histogram[bajt] += 1

    H = 0
    for ni in histogram:
        if ni > 0:
            pi = ni / N
            H -= pi * math.log2(pi)

    return H

def zad_3():
    # 1
    test = b"ala"
    c = rc4(test, b"123")
    d = rc4(c, b"123")
    print("Test RC4:", d == test)

    # 2
    with open("./materialy/rc4.bin", "rb") as f:
        szyfrogram = f.read()
    entropie = dict()
    start = perf_counter()
    for k in product(string.ascii_lowercase, repeat=3):
        odszyfrowane = rc4(szyfrogram[:512], "".join(k).encode())
        entropie[k] = entropia(odszyfrowane)
    koniec = perf_counter()
    
     
    top5 = sorted(entropie.keys(), key=lambda k: (entropie[k], "".join(k)))[:5]
    for i, k in enumerate(top5):
        print(f"{i+1}. klucz={"".join(k)} entropia={entropie[k]}")
    klucz = top5[0]

    # 3
    odszyfrowane = rc4(szyfrogram, "".join(klucz).encode())
    with open("rc4.txt", "wb") as f:
        f.write(odszyfrowane)
    print("Zgodność z kryptogramem:",
      rc4(odszyfrowane, "".join(klucz).encode("ascii")) == szyfrogram)
    print(f"Entropia zaszyfrowanego tekstu = {entropia(szyfrogram)}")
    print(f"Entropia oddzyfrowanego tekstu z kluczem {"".join(klucz)} = {entropia(odszyfrowane)}")
    print(f"Liczba prób = {len(entropie.keys())}")
    print(f"Czas przeszukiwania = {koniec-start}s")


zad_3()