#!/usr/bin/python3
import os
from pathlib import Path

print("Content-Type: text/plain; charset=utf-8")
print()
print(f"Efektywny UID: {os.geteuid()}")
print(f"Efektywny GID: {os.getegid()}")
print(f"Uzytkownik HTTP: {os.environ.get('REMOTE_USER', '(brak)')}")

paths = [
    Path("/lab-data/ogolny.txt"),
    Path("/lab-data/poufny.txt")
]
for path in paths:
    print(f"\nPlik: {path}")
    try:
        contents = path.read_text(encoding="utf-8")
    except PermissionError:
        print("ODMOWA ODCZYTU: brak uprawnien systemowych")
    except OSError as error:
        print(f"BLAD ODCZYTU: {error}")
    else:
        print("ODCZYT OK:")
        print(contents)