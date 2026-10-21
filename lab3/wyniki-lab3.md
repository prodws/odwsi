# Laboratorium 3 — Szyfrowanie blokowe

### Zadanie 1. ECB i CBC

W trybie ECB każy blok był równy z tego powodu, że bloki są niezależne. Ponieważ tekst jawny zawierał powtarzające się 16 bajtowe bloki, one zostały identycznie zaszyfrowane. W trybie CBC wszystkie bloki są różne dlatego, że każdy blok zależy od poprzedniego, co ukrywa powtórzenia bloków tekstu jawnego, pierwszy blok zależy od IV. W obu trybach odzyskane bajty były identyczne z wejściem.

```
Plain: 30313233343536373839414243444546 30313233343536373839414243444546 30313233343536373839414243444546 30313233343536373839414243444546
ECB  : a5ba2b6280d433bccfe6a0461cb88c4e a5ba2b6280d433bccfe6a0461cb88c4e a5ba2b6280d433bccfe6a0461cb88c4e a5ba2b6280d433bccfe6a0461cb88c4e
CBC  : 554c9bf121fc9dbee71b0401e34c9c50 eb28204dc2d2e220d025351d7ecb7755 c0d8ac7af93d66552ae4455a8f3e3264 17c1b7a782ca05801b45969163bef930
```

### Zadanie 2. Szyfrowanie z hasłem

Został wygenerowany klucz na podstawie poniższych parametrów.

```
Hasło:  b'olamakota'
Klucz:  3289a46461e03829d2a6571ece54259ed67294b45cbc3dbe765efb1792c62b7a
Sól:    2649823338978231d8661b5637d34a5e
IV:     9fb50ad918d4ec4854cdf933a54ee35a
```

Wszystkie testy zostały poprawnnie odszyfrowane. Dla pustych danych długość kryptogramu wyniosła 16 bajtów, dla 16 bajtów długość wyniosła 32, a dla pliku "wiadomosc.txt" o rozmiarze 247 bajtów była 256 bajtów. Kryptogramy dla pliku "wiadomosc.txt" zaszyfrowane tym samym hasłem, ale z róznymi parametrami soli i wektora inicjalizującego iv, są zupełnie rózne. Sól zmienia klucz wyprowadzony z tego samego hasła, natomiast IV inicjuje łańcuch CBC i zmienia wynik szyfrowania przy tym samym kluczu. Sól i IV mogą być jawne, ponieważ ich znajomość nie ujawnia hasła ani klucza, muszą być jednak poprawnie zachowane do odszyfrowania. CBC nie zapewnia integralności, ponieważ nie uwierzytelnia kryptogramu i nie gwarantuje wykrycia jego modyfikacji, poprawne dopełnienie PKCS#7 również nie dowodzi autentyczności danych.

Wyniki testów:

```

Test 1:

Długość kryptogramu:  16
Kryptogram:  6d5be1c6a14363486727040dd26228d8

Test 2:
30313233343536373839414243444546
Długość kryptogramu:  32
Kryptogram:  b48168cf84b6986189e73d107ab80f6a 9db816c9108dcbce9dc99b1a3af4c27d

Test 3:
4c61626f7261746f7269756d20333a20 4145532d4342432069206b6c75637a20 7a20686173c582612e0a5a61c5bcc3b3 c582c4872067c499c59b6cc485206a61 c5bac5842e20506c696b206d75736920 7772c3b36369c4872062657a207a6d69 616e792063686fc4876279206a65646e 65676f2062616a74752e0a53c3b36c20 69204956207a61706973756a656d7920 72617a656d207a206b727970746f6772 616d656d2e20486173c5826f20706f7a 6f7374616a6520706f7a6120706c696b 69656d2e0a546f20c4877769637a656e 6965206e6965207a617065776e696120 696e74656772616c6e6fc59b63692064 616e7963682e0a
Długość kryptogramu:  256
Kryptogram:  98d4c4098dcfbda1beb48eff34fd165b f4a238da6b558b2537c49897b0222cbe a60aa1adef3df894b8ea1eadcc4882a2 f761d0f5431ee973c1f5e994b3ba407f 3f6bbff18ac0fa32579c44cc8ff21ba0 1e87e06ccbfb793aba2c4d7cb38b5bb3 53fab31f17b7e8414311785b36ba66d5 912e3695a31a91c5eb8e6a4226c91b38 56c649b89578f9ff5cc0d9ddb546968e 34ddba92ecdd42544a09c9faf575a28c 734c8475101e64c448c33b374a53c309 e0f98234cc938e9c561d7f9948789449 33614c1655e28a412a7c596f2e191c71 1cb340f3509ca7caf997e961de550ebc e2a164c3fa7e959d7a46512acd16dad3 c97decca67f27d38a31bfbd3f43a6244
Sól:    e0f193b4050e9416e16408088d6b0602
IV:     449669c24aa8f92533cf6627c1c6c96d
Długość kryptogramu:  256
Kryptogram:  32426f5ec957a56968632169a1b4ed05 a3fe0e16957c35d50d5b0651826871f5 06aa6a1c1f0f3079f7140c4ebcdd1c69 c20cc27c1dffe048e981e27fe607f700 caacd4d3718eb3a66abf38dc72345584 a0f0586a1fd80789aaa8ba8659b4c2da 19a9585ff0119af60a4bf3b08d321bbe 0f5abe11c73415d442f5aa403b22e594 639206a59703e54651e4e2dd8312931f a994d99974b29cb93c4f69e3f1fe9e7d fa6205ebfe3897d435d918fae3d5f696 0ecb10c0adb1b6a55802c412b939655f d9a6a22c97461f0f5191cc0c879c9b33 3aef90fb1201f063c679a1463825a15e 7d79ac10a6715118f9af82c5ed585577 c531b8e8777e245e03436bdbb5846dc0
```

### Zadanie 3. Odzyskanie słabego klucza

Sprawdzono wszystkie 36 kluczy na pierwszych 4096 bajtach kryptogramu. Entropię obliczono po surowych odszyfrowanych bajtach, bez usuwania dopełnienia z próbki. Pięciu najlepszych kandydatów, uporządkowanych rosnąco według entropii (bity na bajt):

```
m: 4.4536
b: 7.9472
x: 7.9490
o: 7.9493
2: 7.9502
```

Odzyskany znak klucza to `m`, czyli klucz ma postać `mmmmmmmmmmmmmmmm`. Po odszyfrowaniu całego pliku i usunięciu PKCS#7 otrzymano czytelny tekst angielski. Pierwszy wiersz:

```
Record 000. The archive contains laboratory notes about symmetric encryption and careful handling of binary files.
```

Możliwych kluczy jest tylko 36, ponieważ niezależnie wybierany jest jeden znak z 36-elementowego alfabetu, a pozostałe bajty są jego kopiami. Niska entropia pomaga rozpoznać zwykły tekst, ale nie dowodzi poprawności klucza: dane skompresowane mogą mieć wysoką entropię również po poprawnym odszyfrowaniu, więc ranking może wskazać błędnego kandydata.
