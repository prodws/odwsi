# Laboratorium 4 — funkcje skrótu

### 341907 | 28.10.2026 | https://github.com/prodws/odwsi/tree/master/lab4

#### Zadanie 1. Sumy kontrolne

Obliczono sumy SHA-256 plików i porównano je z wartościami zapisanymi w `SHA256SUMS.txt`, wypisując status każdej pozycji.

```
dokumenty/budzet.csv: BŁĄD
dokumenty/dane.bin: OK
dokumenty/harmonogram.txt: BRAK
dokumenty/kontakt.txt: OK
dokumenty/regulamin.txt: OK
Różniące się bity: 131 / 256
```

Rożnicę bitów policzono dla skrotów tekstów ASCII `Ala ma kota.` i `Ola ma kota.`. Suma zapisana obok pliku nie chroni przed celową podmianą, ponieważ atakujący może zmienić plik i sumę; potrzebna jest suma z zaufanego zródła, HMAC z tajnym kluczem lub podpis cyfrowy sprawdzany zaufanym kluczem publicznym.

#### Zadanie 2. Przechowywanie haseł

Wczytano bazę haseł i wykonano cztery testy weryfikacji z porównaniem w stałym czasie.

```
anna, Kasztan-2026: True (oczekiwano: True)
anna, kasztan-2026: False (oczekiwano: False)
piotr, Żółw na łące: True (oczekiwano: True)
kasia, Kasztan-2026: False (oczekiwano: False)
Sole test1 i test2 równe: False
Skróty test1 i test2 równe: False
Weryfikacja test1: True
Weryfikacja test2: True
```

Konta `test1` i `test2` dodano z tym samym hasłem, niezależną losową solą 16 B i 600000 iteracji PBKDF2-HMAC-SHA256 (wynik 32 B). Sól różnicuje skróty jednakowych haseł i ogranicza wykorzystanie gotowych tablic, a liczba iteracji zwiększa koszt każdej próby odgadnięcia hasła.

#### Zadanie 3. Kolizje i paradoks urodzinowy

```
Para (v_oryginał, v_zmieniony): (7282, 1761)
Wspólny h24: aac6b9
h24 niezmienionego oryginału: 9a8fd6
Dopasowania do niego w 8192 wariantach zmienionego: 0
```

Dowolną parę znalezć latwiej, bo porównuje się każdy wariant z wieloma wariantami drugiego zbioru (oczekiwana liczba par: `8192² / 2²⁴ = 4`), a dopasowanie do ustalonego skrótu ma szansę tylko `1 / 2²⁴` na próbę; ogólnie koszt kolizji to około `2^(n/2)`, a dopasowania do ustalonego skrótu około `2^n`.
