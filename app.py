import re
from flask import Flask, abort, redirect, url_for, render_template, request

app = Flask(__name__)

BARANG = {
    1: {"nama": "Osiloskop", "stok": 3, "kategori": "elektronika", "ikon": "📈"},
    2: {"nama": "Multimeter", "stok": 10, "kategori": "elektronika", "ikon": "🔌"},
    3: {"nama": "Router Cisco", "stok": 0, "kategori": "jaringan", "ikon": "📡"},
    4: {"nama": "Kabel LAN", "stok": 25, "kategori": "jaringan", "ikon": "🧵"},
}

USER_TERDAFTAR = ["laboran_budi", "aslab_rina", "dosen_andi", "3124600012"]
DILARANG = ["root", "admin", "laboran"]


def format_valid(u):
    pola_staf = r"(laboran|aslab|dosen)_[a-z]{3,10}"
    pola_nrp = r"\d{10}"
    return bool(re.fullmatch(pola_staf, u) or re.fullmatch(pola_nrp, u))


@app.route("/")
def beranda():
    return render_template("beranda.html")


@app.route("/tentang")
def tentang():
    return render_template("tentang.html")


@app.route("/barang")
def barang():
    return render_template("barang.html", daftar=BARANG)


@app.route("/kontak")
def kontak():
    return render_template("kontak.html")


@app.route("/cek/<username>")
def cek(username):
    u = username.lower()
    if u in DILARANG:
        status = "dilarang"
    elif not format_valid(u):
        status = "tidak_valid"
    elif u in USER_TERDAFTAR:
        status = "dipakai"
    else:
        status = "tersedia"
    return render_template("cek.html", username=username, status=status)


@app.route("/cari")
def cari():
    username = request.args.get("username", "").strip()
    if not username:
        return redirect(url_for("beranda"))
    return redirect(url_for("cek", username=username))


@app.route("/user/<username>")
def user(username):
    u = username.lower()
    if not format_valid(u):
        abort(400)
    if u not in USER_TERDAFTAR:
        abort(404)
    return render_template("user.html", username=username)


@app.route("/barang/<int:id>")
def detail_barang(id):
    item = BARANG.get(id)
    if item is None:
        abort(404)
    return render_template("detail_barang.html", id=id, item=item)


@app.route("/home")
def home():
    return redirect(url_for("beranda"))


@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
