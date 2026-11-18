"""Sejf sekretow i kalkulator - celowo podatna aplikacja do laboratorium 7.

Uruchamiaj wylacznie lokalnie, w kontenerze z pakietu. Dane sa fikcyjne.
"""
import sqlite3
import re

from flask import Flask, render_template, request

app = Flask(__name__)
BAZA = "file:/dane/sekrety.db?mode=ro"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sekret")
def sekret():
    klucz = request.args.get("klucz", "")
    zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
    wiersze, blad = [], None
    try:
        with sqlite3.connect(BAZA, uri=True) as db:
            wiersze = db.execute(zapytanie, (klucz,)).fetchall()
    except sqlite3.Error:
        app.logger.exception("Błąd zapytania do bazy")
        blad = "Nie udało się pobrać danych."
    return render_template("sekret.html", klucz=klucz, zapytanie=zapytanie, wiersze=wiersze, blad=blad)


@app.route("/kalkulator")
def kalkulator():
    wyrazenie = request.args.get("wyrazenie")
    wynik = None
    status = 200

    if wyrazenie is not None:
        liczba = r"-?[0-9]+(?:\.[0-9]+)?"
        wzor = rf"\s*({liczba})\s*([+*/-])\s*({liczba})\s*"
        dopasowanie = None

        if len(wyrazenie) <= 100:
            dopasowanie = re.fullmatch(wzor, wyrazenie)

        if dopasowanie is None:
            wynik = "Błąd: niepoprawne wyrażenie."
            status = 400
        else:
            a = float(dopasowanie.group(1))
            operator = dopasowanie.group(2)
            b = float(dopasowanie.group(3))

            if operator == "+":
                wynik = a + b
            elif operator == "-":
                wynik = a - b
            elif operator == "*":
                wynik = a * b
            elif b == 0:
                wynik = "Błąd: dzielenie przez zero."
                status = 400
            else:
                wynik = a / b

    return render_template(
        "kalkulator.html",
        wyrazenie=wyrazenie if wyrazenie is not None else "",
        wynik=wynik,
    ), status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
