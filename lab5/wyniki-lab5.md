# Laboratorium 5 — kontrola dostępu HTTP i uprawnienia CGI

### 341907 | 04.11.2026 | https://github.com/prodws/odwsi/tree/master/lab5

#### Zadanie 1. Dostęp do katalogów

| Adres                    | Przed zmianą | Po zmianie |
| ------------------------ | ------------ | ---------- |
| `/materialy/`            | 200          | 403        |
| `/materialy/notatka.txt` | 200          | 200        |
| `/wewnetrzne/`           | 200          | 403        |
| `/wewnetrzne/plan.txt`   | 200          | 403        |

Przed zmianą oba katalogi wyświetlały listy plików. Odmowę dostępu potwierdza wpis z logu:

```
web-1  | [Wed Nov 04 11:48:40.625432 2026] [authz_core:error] [pid 11:tid 24] [client 172.18.0.1:50266] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/plan.txt
```

Wyłączenie listowania uniemożliwia wyświetlenie listy plików, ale zachowuje odczyt znanego pliku, natomiast blokada dostępu obejmuje również pliki o znanych nazwach.

#### Zadanie 2. Katalog dostępny na hasło

Dla `/panel/raport.txt` otrzymano 401 bez logowania, 401 z błędnym hasłem i 200 z poprawnym hasłem. Publiczna strona `/` zwróciła 200 bez logowania. Odpowiedź bez logowania zawierała nagłówek `WWW-Authenticate: Basic realm="Laboratorium 5"`.

Basic przez zwykłe HTTP nie chroni hasła w transmisji, ponieważ Base64 jest kodowaniem, a poufność zapewnia dopiero HTTPS. Baza haseł pozostaje lokalna.

#### Zadanie 3. Uprawnienia programu CGI

Przed włączeniem Basic CGI zwróciło 200. Po włączeniu Basic otrzymano 401 bez logowania (CGI nie uruchomiono) i 200 z poprawnym hasłem. Przed Basic i po poprawnym logowaniu efektywne UID i GID wynosiły 2 i 2.

Oba pliki w `/lab-data/` należą do root:daemon (0:2). `ogolny.txt` ma prawa 640 i był odczytywany dzięki prawu odczytu grupy, a `poufny.txt` ma prawa 600 i odczyt był zabroniony, ponieważ czytać może tylko root. Wyniki odczytów przed i po zalogowaniu były takie same.

Logowanie do WWW nie daje CGI praw administratora, ponieważ Basic sprawdza użytkownika HTTP, ale nie zmienia UID/GID procesu, według których system sprawdza prawa plików.

Logi są dostepne w [dowody.md](pliki-dla-studentow/dowody.md).
