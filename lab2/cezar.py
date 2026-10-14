def dCezar(szyfrogram: bytes) -> bytes:
    frekwencje = dict()
    for k in range(256):
        liczba_drukowalnych = 0
        for c in szyfrogram:
            p = (c - k)% 256
            if (p >= 32 and p <= 126) or (p in [9,10,13]) :
                liczba_drukowalnych +=1
        frekwencje[k] = liczba_drukowalnych / len(szyfrogram) if szyfrogram else 0
    
    top5 = sorted(frekwencje.keys(), key=lambda k: (-frekwencje[k], k))[:5]
    for i, k in enumerate(top5):
        poczatek = bytes((c - k) % 256 for c in szyfrogram[:100])
        print(f"{i+1}. klucz={k}, udział={frekwencje[k]}, początek={poczatek.decode('ascii', errors='replace')!r}")
    najlepszy_klucz = top5[1]
    print(f"Najlepszy klucz={najlepszy_klucz}")
    return bytes((c - najlepszy_klucz)% 256 for c in szyfrogram)


def zad_1():
    with open("./materialy/cezar.bin", "rb") as f:
        szyfrogram = f.read()
    odszyfrowane = dCezar(szyfrogram)
    with open("cezar.txt", "wb") as f:
        f.write(odszyfrowane)
    print("Zapisano plik cezar.txt")

zad_1()