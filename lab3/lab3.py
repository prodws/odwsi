import math
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


print("=== Zadanie 1 ===")
# Zadanie 1 — ECB i CBC (około 20 min, 1 pkt)
# 1. Przygotuj 64 bajty: tekst ASCII 0123456789ABCDEF powtórzony cztery razy. Klucz AES-128 to 16 bajtów
# zapisanych szesnastkowo jako 000102030405060708090a0b0c0d0e0f (nie 32 znaki tekstu).
# 2. Zaszyfruj dane w ECB oraz CBC tym samym kluczem. Dla CBC wylosuj bezpiecznie IV o długości 16
# bajtów. Wyłącz dopełnienie: dane są wielokrotnością bloku.
# 3. Wypisz cztery 16-bajtowe bloki każdego kryptogramu w zapisie szesnastkowym. Sprawdź, które bloki się
# powtarzają. Odszyfruj oba kryptogramy i porównaj odzyskane bajty z wejściem; dla CBC użyj pierwotnego IV.
# W raporcie: które bloki były równe w każdym trybie, wynik obu porównań po odszyfrowaniu oraz jedno zdanie
# wyjaśniające obserwację. Pełny wydruk może pozostać w repozytorium


def hex_blocks(d):
    h = d.hex()
    return " ".join(h[i:i+32] for i in range(0, len(h), 32))

def entropy(data):
    counts = [0] * 256
    for byte in data:
        counts[byte] += 1

    result = 0.0
    for count in counts:
        if count > 0:
            probability = count / len(data)
            result -= probability * math.log2(probability)
    return result


hex_string = "000102030405060708090a0b0c0d0e0f"
key = bytes.fromhex(hex_string)
plain = b"0123456789ABCDEF" * 4

aes = AES.new(key, AES.MODE_ECB)
encrypted_ECB = aes.encrypt(plain)

iv = get_random_bytes(16)
aes = AES.new(key, AES.MODE_CBC, iv)
encrypted_CBC = aes.encrypt(plain)


print("Plain: ", hex_blocks(plain))
print("ECB  : ", hex_blocks(encrypted_ECB))
print("CBC  : ", hex_blocks(encrypted_CBC))

assert AES.new(key, AES.MODE_ECB).decrypt(encrypted_ECB) == plain
assert AES.new(key, AES.MODE_CBC, iv).decrypt(encrypted_CBC) == plain


print("=== Zadanie 2 ===")
# 1. Wybierz testowe hasło. Z jego bajtów UTF-8 wyprowadź klucz: PBKDF2-HMAC-SHA256, 200000 iteracji,
# klucz 32 B, losowa sól 16 B. Są to parametry ćwiczenia. Użyj bezpiecznego generatora losowego także do
# osobnego IV 16 B.
# 2. Zaszyfruj AES-CBC z PKCS#7, a następnie odszyfruj i usuń dopełnienie. Zachowaj sól i IV potrzebne do
# odtworzenia klucza i odszyfrowania; wystarczą zmienne w pamięci.
# 3. Samodzielnie napisz i uruchom trzy testy: puste dane, 16 bajtów ASCII 0123456789ABCDEF oraz bajty pliku
# wiadomosc.txt. Sprawdź równość bajtów przed i po operacji oraz długość kryptogramu.
# 4. Zaszyfruj wiadomość jeszcze raz z tym samym hasłem, ale nową solą i IV. Porównaj kryptogramy.
# W raporcie: wyniki trzech testów i długości kryptogramów, wynik porównania dwóch szyfrowań oraz jedno
# zdanie o różnicy między solą a IV. Sól i IV mogą być jawne; CBC nie zapewnia integralności

import hashlib

password = "olamakota".encode('utf-8')
nOfIterations = 200_000

salt = get_random_bytes(16)
iv = get_random_bytes(16)

key = hashlib.pbkdf2_hmac(
    'sha256',
    password,
    salt,
    nOfIterations,
    dklen=32
)


print("Hasło: ", password);
print("Klucz: ", key.hex())
print("Sól:   ", salt.hex())
print("IV:    ", iv.hex())


with open("./wiadomosc.txt", "rb") as f:
    wiadomosc = f.read()
tests = [b"",b"0123456789ABCDEF",wiadomosc]

for i, test in enumerate(tests,1):
    aes = AES.new(key, AES.MODE_CBC, iv)
    paddedP = pad(test, AES.block_size)
    encrypted_CBC = aes.encrypt(paddedP)
    assert unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(encrypted_CBC),AES.block_size) == test
    print(f"\nTest {i}:\n{hex_blocks(test)}")
    assert len(encrypted_CBC) == (len(test) // 16 + 1) * 16
    print("Round trip:", True)
    print(f"Długość kryptogramu: ",len(encrypted_CBC))
    print(f"Kryptogram: ", hex_blocks(encrypted_CBC))

first_ciphertext = encrypted_CBC

salt = get_random_bytes(16)
iv = get_random_bytes(16)

key = hashlib.pbkdf2_hmac(
    'sha256',
    password,
    salt,
    nOfIterations,
    dklen=32
)

print("Sól:   ", salt.hex())
print("IV:    ", iv.hex())

aes = AES.new(key, AES.MODE_CBC, iv)
paddedP = pad(wiadomosc, AES.block_size)
encrypted_CBC2 = aes.encrypt(paddedP)
assert unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(encrypted_CBC2),AES.block_size) == wiadomosc
print(f"Długość kryptogramu: ",len(encrypted_CBC2))
print(f"Kryptogram: ", hex_blocks(encrypted_CBC2))
assert(encrypted_CBC != encrypted_CBC2)

print("=== Zadanie 3 ===")
# Plik slaby_ecb.bin zaszyfrowano AES-128-ECB z PKCS#7. Klucz to jeden znak ASCII ze zbioru
# abcdefghijklmnopqrstuvwxyz0123456789, powtórzony 16 razy. Tekst jawny jest zwykłym tekstem angielskim.
# 1. Sprawdź wszystkie 36 kluczy. Każdym odszyfruj pierwsze 4096 bajtów kryptogramu, bez usuwania
# dopełnienia z próbki.
# 2. Napisz obliczanie entropii bajtów: H = -suma(p_b * log2(p_b)), gdzie p_b to udział bajtu b w próbce.
# Pomijaj bajty o liczności zero. Licz po surowych bajtach, nie po znakach ich zapisu hex.
# 3. Posortuj kandydatów rosnąco według H i wypisz pięciu najlepszych (znak i H). Najlepszym kluczem
# odszyfruj cały plik, usuń PKCS#7 i sprawdź czytelność tekstu. Entropia jest wskazówką, nie dowodem
# poprawności.
# W raporcie: pięciu kandydatów z H do 4 miejsc po przecinku, odzyskany znak klucza i pierwszy wiersz tekstu.
# Dodaj jedno zdanie: dlaczego jest tylko 36 kluczy i czemu ranking może zawieść dla danych
# skompresowanych


with open("./slaby_ecb.bin", "rb") as f:
    ciphertext = f.read()

sample = ciphertext[:4096]
candidates = []
for ch in "abcdefghijklmnopqrstuvwxyz0123456789":
    key = ch.encode("ascii") * 16
    plaintext_sample = AES.new(key, AES.MODE_ECB).decrypt(sample)
    score = entropy(plaintext_sample)
    candidates.append((score, ch))

candidates.sort()
for score, ch in candidates[:5]:
    print(f"{ch}: {score:.4f}")

ch = candidates[0][1]
key = ch.encode("ascii") * 16
plain = unpad(AES.new(key, AES.MODE_ECB).decrypt(ciphertext), AES.block_size)
text = plain.decode("utf-8")
print("Klucz ch:", ch)
print("Pierwsza linia: ", text.splitlines()[0])
with open("./odzyskany_tekst.txt", "wb") as f:
    f.write(plain)
