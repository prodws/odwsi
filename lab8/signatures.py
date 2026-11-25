from glob import glob

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def verify(public_key, data, signature):
    try:
        public_key.verify(signature, data, pss, hashes.SHA256())
        return "OK"
    except InvalidSignature:
        return "BŁĄD"


pss = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32)

with open("./pliki-dla-studentow/klucz_podpisu.pem", "rb") as file:
    public_key = serialization.load_pem_public_key(file.read())

for path in sorted(glob("./pliki-dla-studentow/dokumenty/*.txt")):
    with open(path, "rb") as file:
        data = file.read()
    with open(path + ".sig", "rb") as file:
        signature = file.read()
    print(path.split("/")[-1] + ":", verify(public_key, data, signature))

private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
public_key = private_key.public_key()

data = "Laboratorium 8: prodws".encode("utf-8")
with open("podpis.txt", "wb") as file:
    file.write(data)

signature = private_key.sign(data, pss, hashes.SHA256())
with open("podpis.txt.sig", "wb") as file:
    file.write(signature)

with open("moj_klucz_publiczny.pem", "wb") as file:
    file.write(public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ))

print("Własny podpis przed zmianą:", verify(public_key, data, signature))

changed_data = bytearray(data)
changed_data[0] ^= 1
with open("podpis_zmieniony.txt", "wb") as file:
    file.write(changed_data)

print("Własny podpis po zmianie jednego bajtu:",
      verify(public_key, bytes(changed_data), signature))
