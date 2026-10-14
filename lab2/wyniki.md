# Laboratorium 2 — Kryptografia historyczna

### Zadanie 1. Cezar

Sprawdzono wszystkie 256 przesunięć. 5 najlepszych kandydatów:

```
1. klucz=230, udział=1.0, początek='Wkh#Qljkw#Ihuu|\r\rWkh#qljkw#ihuu|#ohiw#wkh#kduerxu#dw#hohyhq/#dv#lw#kdg#grqh#hyhu|#hyhqlqj#iru#dv#orq'
2. klucz=233, udział=1.0, początek='The Night Ferry\n\nThe night ferry left the harbour at eleven, as it had done every evening for as lon'
3. klucz=228, udział=0.9947534102833159, początek='Ymj%Snlmy%Kjww~\x0f\x0fYmj%snlmy%kjww~%qjky%ymj%mfwgtzw%fy%jqj{js1%fx%ny%mfi%itsj%j{jw~%j{jsnsl%ktw%fx%qts'
4. klucz=229, udział=0.9947534102833159, początek='Xli$Rmklx$Jivv}\x0e\x0eXli$rmklx$jivv}$pijx$xli$levfsyv$ex$ipizir0$ew$mx$leh$hsri$iziv}$izirmrk$jsv$ew$psr'
5. klucz=231, udział=0.9947534102833159, początek='Vjg"Pkijv"Hgtt{\x0c\x0cVjg"pkijv"hgtt{"nghv"vjg"jctdqwt"cv"gngxgp."cu"kv"jcf"fqpg"gxgt{"gxgpkpi"hqt"cu"nqp'
```

Wybrano przesunięcie k=233, ponieważ odszyfrowany tekst zawiera czytelne zdania. Sam udział znaków drukowalnych nie wystarcza do wyboru poprawnego przesunięcia. Entropia histogramu bajtów jest identyczna dla wszystkich przesunięć, ponieważ dodawanie stałej modulo 256 jedynie permutuje wartości bajtów, zachowując ich częstości.

### Zadanie 2. Vigenere bajtowy

Plik `tekst_pl.txt` odczytano binarnie i zaszyfrowano kluczem `ZAMEK`, zapisując wynik w `vigenere.bin`. Odszyfrowany plik jest zgodny ze źródłem.

Wyniki szyfrowania `BRAMABRAMABRAMA`:

Klucz SZYFR: 95ac9a9393 95ac9a9393 95ac9a9393

Klucz KOD: 8da1859890 869d90918c 91968c9c85

Dla klucza `SZYFR` długość klucza wynosi 5 bajtów, tak samo jak długość powtarzanego fragmentu `BRAMA`. Każdy fragment jest szyfrowany tymi samymi pozycjami klucza, co daje identyczne bloki. Klucz `KOD` ma długość 3 bajtów, dlatego kolejne fragmenty trafiają na inne pozycje klucza i dają różne bloki. Powtarzające się bloki mogą ujawniać atakującemu regularność tekstu i informacje o strukturze wiadomości.

### Zadanie 3. RC4

Sprawdzono wszystkie 17 576 kluczy długości trzech małych liter ASCII. Czas przeszukiwania wyniósł około 1.507 sekundy.

Ranking według rosnącej entropii pierwszych 512 bajtów odszyfrowania:

```
1. klucz=tat entropia=4.391044183197801
2. klucz=neg entropia=7.430376480028585
3. klucz=mcn entropia=7.451232162876939
4. klucz=oxo entropia=7.453573837340277
5. klucz=tnx entropia=7.459152626797808
```

Entropia całego kryptogramu: 7.927094 bajt

Entropia całego odszyfrowania kluczem `tat`: 4.325867 bajt

Ponowne szyfrowanie odtwarza kryptogram również dla błędnego klucza, ponieważ RC4 wykorzystuje XOR, a zastosowanie tego samego strumienia klucza dwukrotnie odwraca operację. Ranking entropii może zawieść, ponieważ niska entropia nie gwarantuje poprawnego tekstu.
