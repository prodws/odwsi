# Laboratorium 7 — SQL Injection i Code Injection

### 341907 | 18.11.2026 | https://github.com/prodws/odwsi/tree/master/lab7

Pełne wyniki: [dowody.md](dowody.md).

#### Zadanie 1 - SQL Injection

| Wejście (klucz)                                                     | Liczba wierszy |
| ------------------------------------------------------------------- | -------------- |
| `1234`                                                              | 1              |
| `'`                                                                 | 0 (błąd SQL)   |
| `' OR 1=1 --`                                                       | 4              |
| `' UNION SELECT name, sql FROM sqlite_master WHERE type='table' --` | 2              |
| `' UNION SELECT login, email FROM konta --`                         | 2              |

Po wpisaniu samego apostrofu pojawia się błąd `OperationalError: unrecognized token: "'''"`, bo cudzysłowy pojedyncze w zapytaniu przestają się zgadzać. W tabeli wpisano 0, ponieważ po błędzie aplikacja nie ma wyników do pokazania — wynika to z kodu.

Na podstawie kodu aplikacji zapytanie po wpisaniu `' OR 1=1 --` wygląda tak:

```sql
SELECT wlasciciel, sekret FROM sekrety WHERE klucz = '' OR 1=1 --'
```

W bazie są tabele `sekrety` i `konta`. Tabela `konta` ma kolumny `login`, `rola` i `email` (wszystkie typu `TEXT`). Odczyt kolumn `login` i `email` zwrócił 2 wiersze. Dodatkowe wejście `' UNION SELECT login, rola FROM konta --` też zwróciło 2 wiersze: admin ma rolę `administrator`, a anna — `uzytkownik`.

Apostrof zakończył tekst klucza, `OR 1=1` dodało warunek prawdziwy dla każdego wiersza, a `--` zamieniło resztę zapytania w komentarz, więc aplikacja pokazała wszystkie sekrety.

#### Zadanie 2 - Zapytanie z parametrami

| Wejście (klucz)                                                     | Wiersze przed poprawką | Wiersze po poprawce |
| ------------------------------------------------------------------- | ---------------------- | ------------------- |
| `1234`                                                              | 1                      | 1                   |
| `'`                                                                 | 0 (błąd SQL)           | 0                   |
| `' OR 1=1 --`                                                       | 4                      | 0                   |
| `' UNION SELECT name, sql FROM sqlite_master WHERE type='table' --` | 2                      | 0                   |
| `' UNION SELECT login, email FROM konta --`                         | 2                      | 0                   |
| `d'Artagnan`                                                        | nie wymagane           | 1                   |

Fragmenty poprawionego kodu:

```python
zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
...
wiersze = db.execute(zapytanie, (klucz,)).fetchall()
```

Klucz jest przekazywany osobno jako wartość, więc jego znaki są traktowane jak tekst i nie zmieniają budowy zapytania. Parametr `?` nie może zastąpić nazwy tabeli, bo służy do przekazywania wartości.

Po poprawce żadne z testowanych wejść atakujących nie zwróciło danych, a klucze `1234` i `d'Artagnan` działały poprawnie. Na stronie nie było komunikatów SQLite, a w zapisanych logach nie ma błędów SQLite; wszystkie żądania mają HTTP 200. W kodzie szczegóły błędów są zapisywane przez `app.logger.exception(...)`.

#### Zadanie 3 - Code Injection w kalkulatorze

Przed poprawką funkcja `kalkulator()` obliczała wynik przez `eval(wyrazenie)`, co pozwalało wykonać kod wpisany w formularzu.

| Wyrażenie przed poprawką           | Skrócony wynik                                                  |
| ---------------------------------- | --------------------------------------------------------------- |
| `__import__('os').listdir('/etc')` | Lista plików i katalogów, m.in. `passwd`, `hosts`, `os-release` |
| `open('/etc/os-release').read()`   | Alpine Linux, `VERSION_ID=3.24.4`                               |
| `__import__('os').getuid()`        | UID procesu: `1000`                                             |

Wszystkie trzy wyrażenia pozwoliły odczytać informacje z kontenera lub o procesie aplikacji. UID `1000` potwierdza, że aplikacja działa jako użytkownik bez uprawnień administratora.

Po poprawce kalkulator akceptuje wyłącznie dwie liczby rozdzielone jednym dozwolonym operatorem. Wyniki testów:

| Wejście po poprawce                | HTTP | Wynik                        |
| ---------------------------------- | ---- | ---------------------------- |
| `2+3`                              | 200  | `5.0`                        |
| `7 / 2`                            | 200  | `3.5`                        |
| `-1.5*4`                           | 200  | `-6.0`                       |
| `1/0`                              | 400  | Błąd: dzielenie przez zero.  |
| `__import__('os').listdir('/etc')` | 400  | Błąd: niepoprawne wyrażenie. |
| `open('/etc/os-release').read()`   | 400  | Błąd: niepoprawne wyrażenie. |
| `__import__('os').getuid()`        | 400  | Błąd: niepoprawne wyrażenie. |
| puste pole: `?wyrazenie=`          | 400  | Błąd: niepoprawne wyrażenie. |

Lista dozwolonej składni i operatorów ogranicza wejście do tego, co kalkulator ma wykonać, natomiast blokowanie wybranych słów, np. `import`, można ominąć innym zapisem lub inną konstrukcją języka.
