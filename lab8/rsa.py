from time import perf_counter


def mod_power(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent //= 2
    return result


def factor(number):
    if number % 2 == 0:
        return 2, number // 2
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return divisor, number // divisor
        divisor += 2
    return 1, number


tests_passed = mod_power(4, 13, 497) == 445
for modulus in (2, 7, 497):
    for base in (0, 1, 4, 1000):
        if mod_power(base, 0, modulus) != 1:
            tests_passed = False

path = "./pliki-dla-studentow/male_rsa.txt"
with open(path, encoding="utf-8") as file:
    lines = file.read().splitlines()
n = int(lines[0].split("=")[1])
e = int(lines[1].split("=")[1])
blocks = [int(value) for value in lines[2].split("=")[1].split(",")]

start = perf_counter()
p, q = factor(n)
elapsed = perf_counter() - start
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

data = b""
for block in blocks:
    message = mod_power(block, d, n)
    data += message.to_bytes(4, "big")
text = data.decode("utf-8").rstrip(" ")

print("4^13 mod 497 =", mod_power(4, 13, 497))
print("Testy potęgowania:", "poprawne" if tests_passed else "niepoprawne")
print("p =", p)
print("q =", q)
print("phi =", phi)
print("d =", d)
print(f"Czas faktoryzacji: {elapsed:.6f} s")
print("(e * d) mod phi =", (e * d) % phi)
print("Odszyfrowany tekst:")
print(text)
