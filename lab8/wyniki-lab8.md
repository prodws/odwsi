# Laboratorium 8 — RSA i podpis cyfrowy

### 341907 | 25.11.2026 | https://github.com/prodws/odwsi/tree/master/lab8

#### Zadanie 1 - RSA

Własne potęgowanie metodą kwadratów i mnożeń przeszło testy: `4^13 mod 497 = 445` oraz `a^0 mod n = 1` dla kilku wartości `a` i `n > 1`.

- `p = 1048601`, `q = 1398107`
- Czas faktoryzacji przez dzielenie próbne: `0,029780 s`.
- `φ(n) = 1466053951600`
- `d = 1396416556673`
- Sprawdzenie: `(e · d) mod φ(n) = 1`.

Tekst po odszyfrowaniu bloków, zamianie na 4 bajty big-endian i dekodowaniu UTF-8 (bez końcowego dopełnienia spacjami):

> Klucz RSA o długości 41 bitów rozkładasz na czynniki w ułamku sekundy. Bezpieczne RSA ma co najmniej 2048 bitów.

Dla klucza 2048-bitowego dzielenie próbne wymagałoby w najgorszym przypadku sprawdzenia rzędu 2^1024 dzielników, co jest obliczeniowo niewykonalne.

#### Zadanie 2 - Podpis cyfrowy

| Dokument        | Wynik weryfikacji |
| --------------- | ----------------- |
| `faktura.txt`   | BŁĄD              |
| `protokol.txt`  | OK                |
| `regulamin.txt` | BŁĄD              |
| `umowa.txt`     | OK                |

Własny podpis tekstu `Laboratorium 8: prodws`: OK; po zmianie jednego bajtu w kopii: BŁĄD.

Wygenerowano klucz RSA 3072 bity; podpis używa RSA-PSS, SHA-256, MGF1-SHA-256 i soli 32 B. Klucz prywatny był wyłącznie w pamięci programu.

Poprawny podpis przy kluczu publicznym z niezaufanego źródła nie potwierdza tożsamości osoby, która podpisała dokument.

#### Zadanie 3 - Szyfrowanie hybrydowe

- Długość zaszyfrowanego klucza: paczka `L = 256 B`, odpowiedź `L = 384 B`.
- Pierwszy wiersz odszyfrowanego tekstu: „Gratulacje, paczka odszyfrowana poprawnie.”
- Po zmianie jednego bajtu kryptogramu: ODRZUCONO — weryfikacja tagu GCM nie powiodła się, tekst nie został udostępniony.

Plik szyfrujemy AES, ponieważ jest szybki i obsługuje duże dane, a RSA szyfruje tylko krótki klucz ze względu na ograniczenie długości wiadomości i większy koszt obliczeń.
