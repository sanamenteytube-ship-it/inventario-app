from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
    return "Inventario OK"

if __name__=="__main__":
    print("Iniciando Flask...")
    app.run(debug=True, port=5000)
