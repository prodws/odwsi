from os import urandom

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


oaep = padding.OAEP(
    mgf=padding.MGF1(hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)


def decrypt(data, private_key):
    if len(data) < 2:
        return None
    length = int.from_bytes(data[:2], "big")
    if length != (private_key.key_size + 7) // 8:
        return None
    if len(data) < length + 30:
        return None

    encrypted_key = data[2:2 + length]
    nonce = data[2 + length:14 + length]
    ciphertext = data[14 + length:]
    try:
        aes_key = private_key.decrypt(encrypted_key, oaep)
        if len(aes_key) != 32:
            return None
        return AESGCM(aes_key).decrypt(nonce, ciphertext, None)
    except Exception:
        return None


with open("./pliki-dla-studentow/klucz_prywatny.pem", "rb") as file:
    private_key = serialization.load_pem_private_key(
        file.read(), password=b"Lab8-cwiczenie"
    )
with open("./pliki-dla-studentow/paczka.bin", "rb") as file:
    data = file.read()

plaintext = decrypt(data, private_key)
if plaintext is None:
    print("Paczka odrzucona: niepoprawny format lub szyfrowanie.")
else:
    length = int.from_bytes(data[:2], "big")
    text = plaintext.decode("utf-8")
    print("L paczki:", length)
    print("Odszyfrowany tekst:")
    print(text)

    control_word = text.splitlines()[1].split(":", 1)[1].strip()
    response = (control_word + "\nprodws").encode("utf-8")
    with open("./pliki-dla-studentow/klucz_prowadzacego.pem", "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())

    aes_key = urandom(32)
    nonce = urandom(12)
    encrypted_key = public_key.encrypt(aes_key, oaep)
    ciphertext = AESGCM(aes_key).encrypt(nonce, response, None)
    response_length = len(encrypted_key)
    packet = response_length.to_bytes(2, "big") + encrypted_key + nonce + ciphertext
    with open("odpowiedz.bin", "wb") as file:
        file.write(packet)
    print("L odpowiedzi:", response_length)

    changed_data = bytearray(data)
    changed_data[14 + length] ^= 1
    with open("paczka_zmieniona.bin", "wb") as file:
        file.write(changed_data)
    result = decrypt(bytes(changed_data), private_key)
    print("Po zmianie jednego bajtu kryptogramu:",
          "ODRZUCONO" if result is None else "ZAAKCEPTOWANO")
