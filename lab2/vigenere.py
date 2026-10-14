def vigenere(dane: bytes, klucz: str, szyfrowanie: bool) -> bytes:
    klucz_bajty = klucz.encode("utf-8")

    znak = 1 if szyfrowanie else -1
    m = len(klucz_bajty)
    wynik = []
    for i in range(len(dane)):
        wynik.append((dane[i] + znak * klucz_bajty[i % m]) % 256)
    return bytes(wynik)

def zad_2():
    # 1
    with open("materialy/tekst_pl.txt", "rb") as f:
        tekst_pl = f.read()
    szyfrogram = vigenere(tekst_pl, "ZAMEK", True)
    with open("vigenere.bin", "wb") as f:
            f.write(szyfrogram)

    odszyfrowane = vigenere(szyfrogram, "ZAMEK", False)

    print(f"Odszyfrowany tekst_pl.txt jest identyczny: {tekst_pl == odszyfrowane}")

    print("Test pustych danych:",  vigenere(b"", "ZAMEK", True) == b"")

    test = bytes([0, 255])
    szyfrogram_test = vigenere(test, "ZAMEK", True)
    odszyfrowane_test = vigenere(szyfrogram_test, "ZAMEK", False)

    print("Test bajtów 0 i 255:", odszyfrowane_test == test)

    # 2
    ciag = b"BRAMABRAMABRAMA"
    k1 = "SZYFR"
    k2 = "KOD"

    szyfrogramK1 = vigenere(ciag, k1, True)
    szyfrogramK2 = vigenere(ciag, k2, True)
    for k, szyfrogram in [(k1, szyfrogramK1), (k2, szyfrogramK2)]:
        print(f"Klucz {k}:")
        for i in range(0, len(szyfrogram), 5):
            print(szyfrogram[i:i+5].hex())

zad_2()
