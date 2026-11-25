# Zadanie 1

`rsa.py`

```
4^13 mod 497 = 445
Testy potęgowania: poprawne
p = 1048601
q = 1398107
phi = 1466053951600
d = 1396416556673
Czas faktoryzacji: 0.029780 s
(e * d) mod phi = 1
Odszyfrowany tekst:
Klucz RSA o długości 41 bitów rozkładasz na czynniki w ułamku sekundy. Bezpieczne RSA ma co najmniej 2048 bitów.
```

# Zadanie 2

`signatures.py`

```
faktura.txt: BŁĄD
protokol.txt: OK
regulamin.txt: BŁĄD
umowa.txt: OK
Własny podpis przed zmianą: OK
Własny podpis po zmianie jednego bajtu: BŁĄD
```

# Zadanie 3

`hybrid.py`

```
L paczki: 256
Odszyfrowany tekst:
Gratulacje, paczka odszyfrowana poprawnie.
Słowo kontrolne do odpowiedzi: [pominięto]
Klucz AES tej wiadomości był losowy i zabezpieczony tylko algorytmem RSA-OAEP.

L odpowiedzi: 384
Po zmianie jednego bajtu kryptogramu: ODRZUCONO
```

