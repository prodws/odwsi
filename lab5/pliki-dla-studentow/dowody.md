# Zadanie 1

## Przed zmianami

```

$ curl -i http://127.0.0.1:8080/materialy/
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:40:16 GMT
Server: Apache
Content-Length: 305
Content-Type: text/html;charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Index of /materialy</title>
 </head>
 <body>
<h1>Index of /materialy</h1>
<ul><li><a href="/"> Parent Directory</a></li>
<li><a href="notatka.txt"> notatka.txt</a></li>
</ul>
</body></html>


$ curl -i http://127.0.0.1:8080/materialy/notatka.txt
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:41:05 GMT
Server: Apache
Last-Modified: Tue, 03 Nov 2026 20:13:00 GMT
ETag: "45-65f64e397ab00"
Accept-Ranges: bytes
Content-Length: 69
Content-Type: text/plain; charset=UTF-8

Publiczna notatka: ten plik ma pozostac dostepny pod znanym adresem.


$ curl -i http://127.0.0.1:8080/wewnetrzne/
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:41:37 GMT
Server: Apache
Content-Length: 301
Content-Type: text/html;charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Index of /wewnetrzne</title>
 </head>
 <body>
<h1>Index of /wewnetrzne</h1>
<ul><li><a href="/"> Parent Directory</a></li>
<li><a href="plan.txt"> plan.txt</a></li>
</ul>
</body></html>


$ curl -i http://127.0.0.1:8080/wewnetrzne/plan.txt
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:41:47 GMT
Server: Apache
Last-Modified: Tue, 03 Nov 2026 20:13:00 GMT
ETag: "3a-65f64e397ab00"
Accept-Ranges: bytes
Content-Length: 58
Content-Type: text/plain; charset=UTF-8

Fikcyjny plan: ten katalog ma byc niedostepny przez HTTP.
```

## Wyłączenie listowania

```

$ curl -i http://127.0.0.1:8080/materialy/
HTTP/1.1 403 Forbidden
Date: Wed, 04 Nov 2026 11:45:49 GMT
Server: Apache
Content-Length: 239
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>

<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body></html>

$ curl -i http://127.0.0.1:8080/materialy/notatka.txt
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:46:03 GMT
Server: Apache
Last-Modified: Tue, 03 Nov 2026 20:13:00 GMT
ETag: "45-65f64e397ab00"
Accept-Ranges: bytes
Content-Length: 69
Content-Type: text/plain; charset=UTF-8

Publiczna notatka: ten plik ma pozostac dostepny pod znanym adresem.
```

## Blokada dostępu

```

$ curl -i http://127.0.0.1:8080/wewnetrzne/
HTTP/1.1 403 Forbidden
Date: Wed, 04 Nov 2026 11:48:37 GMT
Server: Apache
Content-Length: 239
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body></html>



$ curl -i http://127.0.0.1:8080/wewnetrzne/plan.txt
HTTP/1.1 403 Forbidden
Date: Wed, 04 Nov 2026 11:48:40 GMT
Server: Apache
Content-Length: 239
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body></html>
```

## Potwierdzenie w logach

```
pliki-dla-studentow ❯ docker compose logs --tail 30 web
web-1  | 172.18.0.1 - - [04/Nov/2026:11:32:39 +0000] "GET /wewnetrzne/ HTTP/1.1" 200 301
web-1  | 172.18.0.1 - - [04/Nov/2026:11:33:03 +0000] "GET /wewnetrzne/ HTTP/1.1" 200 301
web-1  | 172.18.0.1 - - [04/Nov/2026:11:33:04 +0000] "GET /wewnetrzne/ HTTP/1.1" 200 301
web-1  | 172.18.0.1 - - [04/Nov/2026:11:33:39 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:38:52 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:39:10 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:39:53 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:40:14 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:40:16 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:40:38 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:41:05 +0000] "GET /materialy/notatka.txt HTTP/1.1" 200 69
web-1  | 172.18.0.1 - - [04/Nov/2026:11:41:20 +0000] "GET /wewnetrzne/ HTTP/1.1" 200 301
web-1  | 172.18.0.1 - - [04/Nov/2026:11:41:37 +0000] "GET /wewnetrzne/ HTTP/1.1" 200 301
web-1  | 172.18.0.1 - - [04/Nov/2026:11:41:47 +0000] "GET /wewnetrzne/plan.txt HTTP/1.1" 200 58
web-1  | 172.18.0.1 - - [04/Nov/2026:11:43:30 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | [Wed Nov 04 11:45:00.589607 2026] [mpm_event:notice] [pid 1:tid 1] AH00492: caught SIGWINCH, shutting down gracefully
web-1  | [Wed Nov 04 11:45:01.931440 2026] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.69 (Unix) configured -- resuming normal operations
web-1  | [Wed Nov 04 11:45:01.931461 2026] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
web-1  | [Wed Nov 04 11:45:49.084534 2026] [autoindex:error] [pid 10:tid 18] [client 172.18.0.1:51936] AH01276: Cannot serve directory /usr/local/apache2/htdocs/materialy/: No matching DirectoryIndex (index.html) found, and server-generated directory index forbidden by Options directive
web-1  | 172.18.0.1 - - [04/Nov/2026:11:45:49 +0000] "GET /materialy/ HTTP/1.1" 403 239
web-1  | 172.18.0.1 - - [04/Nov/2026:11:46:03 +0000] "GET /materialy/notatka.txt HTTP/1.1" 200 69
web-1  | [Wed Nov 04 11:46:45.396850 2026] [autoindex:error] [pid 10:tid 25] [client 172.18.0.1:51366] AH01276: Cannot serve directory /usr/local/apache2/htdocs/materialy/: No matching DirectoryIndex (index.html) found, and server-generated directory index forbidden by Options directive, referer: http://127.0.0.1:8080/
web-1  | 172.18.0.1 - - [04/Nov/2026:11:46:45 +0000] "GET /materialy/ HTTP/1.1" 403 239
web-1  | [Wed Nov 04 11:48:22.123153 2026] [mpm_event:notice] [pid 1:tid 1] AH00492: caught SIGWINCH, shutting down gracefully
web-1  | [Wed Nov 04 11:48:23.475553 2026] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.69 (Unix) configured -- resuming normal operations
web-1  | [Wed Nov 04 11:48:23.475585 2026] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
web-1  | [Wed Nov 04 11:48:37.037901 2026] [authz_core:error] [pid 10:tid 18] [client 172.18.0.1:38310] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/
web-1  | 172.18.0.1 - - [04/Nov/2026:11:48:37 +0000] "GET /wewnetrzne/ HTTP/1.1" 403 239
web-1  | [Wed Nov 04 11:48:40.625432 2026] [authz_core:error] [pid 11:tid 24] [client 172.18.0.1:50266] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/plan.txt
web-1  | 172.18.0.1 - - [04/Nov/2026:11:48:40 +0000] "GET /wewnetrzne/plan.txt HTTP/1.1" 403 239
```

# Zadanie 2

## Utworzenie konta i próba bez logowania

```

docker compose run --rm --no-deps narzedzia -cB /auth/uzytkownicy student
[+] run 1/1
 ✔ Container pliki-dla-studentow-narzedzia-run-ae80ad6bd148 Created    
 
 curl -i http://127.0.0.1:8080/panel/raport.txt                                     0.1s
New password: 
Re-type new password: 
Adding password for user student
HTTP/1.1 401 Unauthorized
Date: Wed, 04 Nov 2026 12:01:38 GMT
Server: Apache
WWW-Authenticate: Basic realm="Laboratorium 5"
Content-Length: 421
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>401 Unauthorized</title>
</head><body>
<h1>Unauthorized</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
</body></html>
```

## Błędne hasło

```
curl -i -u student http://127.0.0.1:8080/panel/raport.txt | tee -a dowody.txt
HTTP/1.1 401 Unauthorized
Date: Wed, 04 Nov 2026 12:02:21 GMT
Server: Apache
WWW-Authenticate: Basic realm="Laboratorium 5"
Content-Length: 421
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>401 Unauthorized</title>
</head><body>
<h1>Unauthorized</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
</body></html>
```

## Poprawne hasło

```
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 12:02:57 GMT
Server: Apache
Last-Modified: Tue, 03 Nov 2026 20:13:00 GMT
ETag: "3a-65f64e397ab00"
Accept-Ranges: bytes
Content-Length: 58
Content-Type: text/plain; charset=UTF-8

Raport cwiczeniowy: dostep po poprawnym uwierzytelnieniu.
```

## Strona publiczna

```
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 12:04:16 GMT
Server: Apache
Last-Modified: Tue, 03 Nov 2026 20:13:00 GMT
ETag: "15f-65f64e397ab00"
Accept-Ranges: bytes
Content-Length: 351
Content-Type: text/html; charset=UTF-8

<!doctype html>
<html lang="pl"><meta charset="utf-8"><title>Laboratorium 5</title>
<h1>Laboratorium 5: serwer WWW działa</h1>
<p>Materiały ćwiczeniowe do konfiguracji dostępu w Apache.</p>
<ul><li><a href="/materialy/">Materiały</a></li>
<li><a href="/wewnetrzne/">Wewnętrzne</a></li>
<li><a href="/panel/raport.txt">Panel</a></li></ul></html>
```

## Potwierdzenie w logach

```
pliki-dla-studentow ❯ docker compose logs --tail 30 web
web-1  | 172.18.0.1 - - [04/Nov/2026:11:40:16 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:40:38 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | 172.18.0.1 - - [04/Nov/2026:11:41:05 +0000] "GET /materialy/notatka.txt HTTP/1.1" 200 69
web-1  | 172.18.0.1 - - [04/Nov/2026:11:41:20 +0000] "GET /wewnetrzne/ HTTP/1.1" 200 301
web-1  | 172.18.0.1 - - [04/Nov/2026:11:41:37 +0000] "GET /wewnetrzne/ HTTP/1.1" 200 301
web-1  | 172.18.0.1 - - [04/Nov/2026:11:41:47 +0000] "GET /wewnetrzne/plan.txt HTTP/1.1" 200 58
web-1  | 172.18.0.1 - - [04/Nov/2026:11:43:30 +0000] "GET /materialy/ HTTP/1.1" 200 305
web-1  | [Wed Nov 04 11:45:00.589607 2026] [mpm_event:notice] [pid 1:tid 1] AH00492: caught SIGWINCH, shutting down gracefully
web-1  | [Wed Nov 04 11:45:01.931440 2026] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.69 (Unix) configured -- resuming normal operations
web-1  | [Wed Nov 04 11:45:01.931461 2026] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
web-1  | [Wed Nov 04 11:45:49.084534 2026] [autoindex:error] [pid 10:tid 18] [client 172.18.0.1:51936] AH01276: Cannot serve directory /usr/local/apache2/htdocs/materialy/: No matching DirectoryIndex (index.html) found, and server-generated directory index forbidden by Options directive
web-1  | 172.18.0.1 - - [04/Nov/2026:11:45:49 +0000] "GET /materialy/ HTTP/1.1" 403 239
web-1  | 172.18.0.1 - - [04/Nov/2026:11:46:03 +0000] "GET /materialy/notatka.txt HTTP/1.1" 200 69
web-1  | [Wed Nov 04 11:46:45.396850 2026] [autoindex:error] [pid 10:tid 25] [client 172.18.0.1:51366] AH01276: Cannot serve directory /usr/local/apache2/htdocs/materialy/: No matching DirectoryIndex (index.html) found, and server-generated directory index forbidden by Options directive, referer: http://127.0.0.1:8080/
web-1  | 172.18.0.1 - - [04/Nov/2026:11:46:45 +0000] "GET /materialy/ HTTP/1.1" 403 239
web-1  | [Wed Nov 04 11:48:22.123153 2026] [mpm_event:notice] [pid 1:tid 1] AH00492: caught SIGWINCH, shutting down gracefully
web-1  | [Wed Nov 04 11:48:23.475553 2026] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.69 (Unix) configured -- resuming normal operations
web-1  | [Wed Nov 04 11:48:23.475585 2026] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
web-1  | [Wed Nov 04 11:48:37.037901 2026] [authz_core:error] [pid 10:tid 18] [client 172.18.0.1:38310] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/
web-1  | 172.18.0.1 - - [04/Nov/2026:11:48:37 +0000] "GET /wewnetrzne/ HTTP/1.1" 403 239
web-1  | [Wed Nov 04 11:48:40.625432 2026] [authz_core:error] [pid 11:tid 24] [client 172.18.0.1:50266] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/plan.txt
web-1  | 172.18.0.1 - - [04/Nov/2026:11:48:40 +0000] "GET /wewnetrzne/plan.txt HTTP/1.1" 403 239
web-1  | [Wed Nov 04 12:01:28.392983 2026] [mpm_event:notice] [pid 1:tid 1] AH00492: caught SIGWINCH, shutting down gracefully
web-1  | [Wed Nov 04 12:01:29.770695 2026] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.69 (Unix) configured -- resuming normal operations
web-1  | [Wed Nov 04 12:01:29.770718 2026] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
web-1  | 172.18.0.1 - - [04/Nov/2026:12:01:38 +0000] "GET /panel/raport.txt HTTP/1.1" 401 421
web-1  | [Wed Nov 04 12:02:21.736095 2026] [auth_basic:error] [pid 10:tid 30] [client 172.18.0.1:57088] AH01617: user student: authentication failure for "/panel/raport.txt": Password Mismatch
web-1  | 172.18.0.1 - student [04/Nov/2026:12:02:21 +0000] "GET /panel/raport.txt HTTP/1.1" 401 421
web-1  | 172.18.0.1 - student [04/Nov/2026:12:02:57 +0000] "GET /panel/raport.txt HTTP/1.1" 200 58
web-1  | 172.18.0.1 - - [04/Nov/2026:12:04:16 +0000] "GET / HTTP/1.1" 200 351
```

# Zadanie 3

## CGI przed włączeniem Basic

```
curl -i http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 12:15:20 GMT
Server: Apache
Transfer-Encoding: chunked
Content-Type: text/plain; charset=utf-8

Efektywny UID: 2
Efektywny GID: 2
Uzytkownik HTTP: (brak)

Plik: /lab-data/ogolny.txt
ODCZYT OK:
LAB05: dokument dostepny dla grupy procesu WWW.


Plik: /lab-data/poufny.txt
ODMOWA ODCZYTU: brak uprawnien systemowych
```

## Właściciele i prawa plików

```
docker compose exec web ls -ln /lab-data/
total 8
-rw-r-----    1 0        2               48 Nov  3 20:13 ogolny.txt
-rw-------    1 0        2               61 Nov  3 20:13 poufny.txt
```

## bez logowania

```
curl -i http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 401 Unauthorized
Date: Wed, 04 Nov 2026 12:21:09 GMT
Server: Apache
WWW-Authenticate: Basic realm="Laboratorium 5"
Content-Length: 421
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>401 Unauthorized</title>
</head><body>
<h1>Unauthorized</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
</body></html>
```

## poprawne hasło

```
curl -i -u student http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
Enter host password for user 'student':
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 12:21:42 GMT
Server: Apache
Transfer-Encoding: chunked
Content-Type: text/plain; charset=utf-8

Efektywny UID: 2
Efektywny GID: 2
Uzytkownik HTTP: student

Plik: /lab-data/ogolny.txt
ODCZYT OK:
LAB05: dokument dostepny dla grupy procesu WWW.


Plik: /lab-data/poufny.txt
ODMOWA ODCZYTU: brak uprawnien systemowych
```

## Potwierdzenie w logach

```
docker compose logs --tail 30 web
web-1  | [Wed Nov 04 12:14:49.986387 2026] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.69 (Unix) configured -- resuming normal operations
web-1  | [Wed Nov 04 12:14:49.986424 2026] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
web-1  | 172.18.0.1 - - [04/Nov/2026:12:15:20 +0000] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 200 217
web-1  | [Wed Nov 04 12:17:18.708537 2026] [mpm_event:notice] [pid 1:tid 1] AH00492: caught SIGWINCH, shutting down gracefully
web-1  | [Wed Nov 04 12:17:20.059885 2026] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.69 (Unix) configured -- resuming normal operations
web-1  | [Wed Nov 04 12:17:20.059917 2026] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
web-1  | [Wed Nov 04 12:17:42.949957 2026] [auth_basic:error] [pid 10:tid 20] [client 172.18.0.1:57682] AH01615: need AuthName: /cgi-bin/uprawnienia.cgi
web-1  | 172.18.0.1 - - [04/Nov/2026:12:17:42 +0000] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 500 571
web-1  | [Wed Nov 04 12:18:34.129560 2026] [auth_basic:error] [pid 11:tid 29] [client 172.18.0.1:40188] AH01615: need AuthName: /cgi-bin/uprawnienia.cgi
web-1  | 172.18.0.1 - - [04/Nov/2026:12:18:34 +0000] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 500 571
web-1  | [Wed Nov 04 12:20:54.216533 2026] [mpm_event:notice] [pid 1:tid 1] AH00492: caught SIGWINCH, shutting down gracefully
web-1  | [Wed Nov 04 12:20:55.586921 2026] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.69 (Unix) configured -- resuming normal operations
web-1  | [Wed Nov 04 12:20:55.586940 2026] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
web-1  | 172.18.0.1 - - [04/Nov/2026:12:21:09 +0000] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 401 421
web-1  | 172.18.0.1 - student [04/Nov/2026:12:21:42 +0000] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 200 218
```
