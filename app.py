from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DB_URL = os.environ.get("DATABASE_URL", "sqlite:///inventario.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(500))

@app.route("/")
def home():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template("index.html", products=products)

@app.route("/add", methods=["POST"])
def add():
    p = Product(
        name=request.form["name"],
        sku=request.form["sku"],
        stock=int(request.form["stock"]),
        price=float(request.form["price"] or 0),
        image_url=request.form.get("image_url") or None,
    )
    db.session.add(p)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/edit/<int:pid>", methods=["GET", "POST"])
def edit(pid):
    p = Product.query.get_or_404(pid)
    if request.method == "POST":
        p.name = request.form["name"]
        p.sku = request.form["sku"]
        p.stock = int(request.form["stock"])
        p.price = float(request.form["price"] or 0)
        p.image_url = request.form.get("image_url") or None
        db.session.commit()
        return redirect(url_for("home"))
    return f"""
    <form method='post' style='max-width:520px;margin:2rem auto;font-family:sans-serif'>
    <h3>Editar producto</h3>
    <input name='name' value='{p.name}' required>
    <input name='sku' value='{p.sku}' required>
    <input name='stock' type='number' value='{p.stock}' required>
    <input name='price' type='number' step='0.01' value='{p.price}' required>
    <input name='image_url' value='{p.image_url or ""}'>
    <button>Guardar</button> &nbsp; <a href='/'>Cancelar</a>
    </form>
    """

@app.route("/delete/<int:pid>")
def delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/initdb")
def initdb():
    db.create_all()
    return "DB OK"

if __name__ == "__main__":
    app.run(debug=True, port=5000)