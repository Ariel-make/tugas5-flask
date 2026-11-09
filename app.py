import re
from flask import Flask, abort, redirect, url_for

app = Flask(__name__)

BARANG = {
    1: {"nama": "Osiloskop", "stok": 3},
    2: {"nama": "Multimeter", "stok": 10},
    3: {"nama": "Router Cisco", "stok": 0},
}

USER_TERDAFTAR = ["laboran_budi", "aslab_rina", "dosen_andi", "3124600012"]
DILARANG = ["root", "admin", "laboran"]

def format_valid(u):
    pola_staf = r"(laboran|aslab|dosen)_[a-z]{3,10}"
    pola_nrp = r"\d{10}"
    return bool(re.fullmatch(pola_staf, u) or re.fullmatch(pola_nrp, u))

@app.route("/")
def beranda():
    return "Beranda - Inventaris Lab Kampus"

@app.route("/tentang")
def tentang():
    return "Tentang Lab"

@app.route("/barang")
def barang():
    return "Daftar Barang Lab"

@app.route("/kontak")
def kontak():
    return "Kontak Laboran"

@app.route("/cek/<username>")
def cek(username):
    u = username.lower()
    if u in DILARANG:
        return f"'{username}' dilarang dipakai"
    if not format_valid(u):
        return f"'{username}' tidak valid"
    if u in USER_TERDAFTAR:
        return f"'{username}' sudah dipakai"
    return f"'{username}' tersedia"

@app.route("/user/<username>")
def user(username):
    u = username.lower()
    if not format_valid(u):
        abort(400)
    if u not in USER_TERDAFTAR:
        abort(404)
    return f"Profil: {username}"

@app.route("/barang/<int:id>")
def detail_barang(id):
    item = BARANG.get(id)
    if item is None:
        abort(404)
    return f"{item['nama']} - stok {item['stok']}"

@app.route("/home")
def home():
    return redirect(url_for("beranda"))

@app.errorhandler(404)
def not_found(e):
    return "Halaman atau barang tidak ditemukan di sistem lab", 404

if __name__ == "__main__":
    app.run(debug=True)
