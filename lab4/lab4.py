import hashlib
import hmac
import os
import secrets


# Zadanie 1 — Sumy kontrolne (około 20 min, 1 pkt)
# Plik SHA256SUMS.txt ma format programu sha256sum: w każdym wierszu 64 znaki hex
# skrótu SHA-256, dwie spacje i ścieżka względem katalogu z SHA256SUMS.txt.
# 1. Napisz funkcję liczącą SHA-256 pliku. Możesz wczytać cały plik naraz.
# 2. Dla każdego wiersza wypisz ścieżkę i status: OK (skrót zgodny), BŁĄD (inny
# skrót) albo BRAK (pliku nie ma). Brakujący plik nie może przerwać programu.
# 3. Oblicz SHA-256 tekstów ASCII "Ala ma kota." i "Ola ma kota.". Policz, ile
# z 256 bitów różni się w obu skrótach (XOR skrótów i liczba jedynek).
# Samokontrola: porównaj statusy z wynikiem sha256sum -c SHA256SUMS.txt.
# W raporcie: status każdego pliku, liczba różniących się bitów oraz jedno zdanie:
# dlaczego suma obok pliku nie chroni przed celową podmianą i czego użyć zamiast niej.


def sha256_file(path):
    with open(path, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()


def verify_checksums(checksum_file):
    with open(checksum_file, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    for line in lines:
        expected, path = line.split("  ", 1)
        file_path = "./dane/" + path
        if not os.path.isfile(file_path):
            status = "BRAK"
        elif sha256_file(file_path) == expected.lower():
            status = "OK"
        else:
            status = "BŁĄD"
        print(f"{path}: {status}")


def count_different_bits(first, second):
    return (int.from_bytes(first, "big") ^ int.from_bytes(second, "big")).bit_count()


print("=== Zadanie 1 ===")
verify_checksums("./dane/SHA256SUMS.txt")

first = hashlib.sha256(b"Ala ma kota.").digest()
second = hashlib.sha256(b"Ola ma kota.").digest()
print(f"Różniące się bity: {count_different_bits(first, second)} / 256")


# Zadanie 2 — Przechowywanie haseł (około 25 min, 1 pkt)
# Plik hasla.txt zawiera rekordy login:iteracje:sól_hex:skrót_hex. Skrót to
# PBKDF2-HMAC-SHA256 z bajtów UTF-8 hasła, solą 16 B i liczbą iteracji z rekordu;
# wynik ma 32 B.
# 1. Wczytaj bazę i napisz weryfikuj(login, hasło): wylicz skrót z parametrami
# rekordu i porównaj go z zapisanym funkcją biblioteczną w stałym czasie.
# Nieznany login daje fałsz. Sprawdź cztery przypadki:
# - anna, Kasztan-2026 -> prawda;
# - anna, kasztan-2026 -> fałsz;
# - piotr, Żółw na łące -> prawda (kod źródłowy zapisany w UTF-8);
# - kasia, Kasztan-2026 -> fałsz.
# 2. Napisz dodaj(login, hasło): sól 16 B z bezpiecznego generatora, 600000
# iteracji, rekord w tym samym formacie. Dodaj test1 i test2 z tym samym hasłem,
# porównaj ich sole i skróty oraz zweryfikuj oba konta. Zapis do pliku niewymagany.
# W raporcie: wyniki czterech testów, porównania soli i skrótów nowych kont,
# weryfikacji obu kont oraz jedno zdanie: co daje sól, a co liczba iteracji.
# Nie przepisuj pełnych rekordów.


def load_passwords(path):
    with open(path, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    records = {}
    for line in lines:
        login, iterations, salt_hex, digest_hex = line.split(":")
        iterations = int(iterations)
        salt = bytes.fromhex(salt_hex)
        digest = bytes.fromhex(digest_hex)
        records[login] = (iterations, salt, digest)
    return records


def verify_password(login, password):
    if login not in password_db:
        return False
    iterations, salt, stored_digest = password_db[login]
    computed = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations, dklen=32
    )
    return hmac.compare_digest(computed, stored_digest)


def add_account(login, password):
    salt = secrets.token_bytes(16)
    iterations = 600_000
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations, dklen=32
    )
    password_db[login] = (iterations, salt, digest)
    return f"{login}:{iterations}:{salt.hex()}:{digest.hex()}"


print("\n=== Zadanie 2 ===")
password_db = load_passwords("./dane/hasla.txt")
tests = [
    ("anna", "Kasztan-2026", True),
    ("anna", "kasztan-2026", False),
    ("piotr", "Żółw na łące", True),
    ("kasia", "Kasztan-2026", False),
]
for login, password, expected in tests:
    print(f"{login}, {password}: {verify_password(login, password)} (oczekiwano: {expected})")

password = "Wspolne-haslo-2026"
add_account("test1", password)
add_account("test2", password)
print(f"Sole test1 i test2 równe: {password_db['test1'][1] == password_db['test2'][1]}")
print(f"Skróty test1 i test2 równe: {password_db['test1'][2] == password_db['test2'][2]}")
for login in ("test1", "test2"):
    print(f"Weryfikacja {login}: {verify_password(login, password)}")


# Zadanie 3 — Kolizje i paradoks urodzinowy (około 25 min, 1 pkt)
# h24(dane) to pierwsze 3 bajty SHA-256(dane), czyli 6 pierwszych znaków hex.
# Pliki oryginal.txt i zmieniony.txt mają po 13 wierszy zakończonych bajtem LF
# i różnią się treścią. Wariant v, dla 0 <= v < 8192: dla każdego wiersza i=0..12
# dopisz jedną spację przed jego LF, jeśli (v >> i) & 1 wynosi 1. Pozostałe bajty
# zostają bez zmian. Wariant 0 to plik bez zmian.
# 1. Policz h24 wszystkich 8192 wariantów oryginału i zapamiętaj je w słowniku
# h24 -> v. Gdy skrót się powtórzy, wystarczy zachować jeden numer wariantu.
# 2. Przeglądaj warianty zmienionego dokumentu i znajdź jedną parę
# (v_oryginał, v_zmieniony) o równym h24. Wypisz parę i jej h24. Dowolna poprawna
# para jest akceptowana; nie trzeba sortować par ani zapisywać wariantów do plików.
# 3. Sprawdź wszystkie 8192 warianty zmienionego dokumentu i policz, ile ma h24
# równy h24 niezmienionego oryginału (wariant 0). Możesz kontynuować tę samą pętlę.
# W raporcie: para z h24, wynik kroku 3 oraz jedno zdanie: dlaczego znalezienie
# dowolnej pary jest znacznie łatwiejsze niż dopasowanie do ustalonego skrótu.


def h24(data):
    return hashlib.sha256(data).digest()[:3]


def read_lines(path):
    with open(path, "rb") as file:
        data = file.read()
    return data.split(b"\n")[:-1]


def make_variant(lines, variant_id):
    data = b""
    for line_index, line in enumerate(lines):
        if (variant_id >> line_index) & 1:
            line += b" "
        data += line + b"\n"
    return data


def find_collision(original, modified):
    hashes = {}
    for variant_id in range(8192):
        hashes[h24(make_variant(original, variant_id))] = variant_id

    target = h24(make_variant(original, 0))
    pair = None
    match_count = 0
    for variant_id in range(8192):
        digest = h24(make_variant(modified, variant_id))
        if pair is None and digest in hashes:
            pair = (hashes[digest], variant_id, digest)
        if digest == target:
            match_count += 1
    return pair, target, match_count


print("\n=== Zadanie 3 ===")
original = read_lines("./dane/oryginal.txt")
modified = read_lines("./dane/zmieniony.txt")
pair, target, match_count = find_collision(original, modified)
if pair is None:
    print("Nie znaleziono pary kolizyjnej w tych zbiorach wariantów.")
else:
    original_variant_id, modified_variant_id, digest = pair
    print(f"Para (v_oryginał, v_zmieniony): ({original_variant_id}, {modified_variant_id})")
    print(f"Wspólny h24: {digest.hex()}")
print(f"h24 niezmienionego oryginału: {target.hex()}")
print(f"Dopasowania do niego w 8192 wariantach zmienionego: {match_count}")