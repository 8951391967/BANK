from flask import Flask, render_template, request, redirect
import json
import random

app = Flask(__name__)
DATA_FILE = "data.json"


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        balance = float(request.form["balance"])
        acc_no = random.randint(100000, 999999)

        data = load_data()
        data["accounts"].append({
            "acc_no": acc_no,
            "name": name,
            "balance": balance
        })
        save_data(data)

        return redirect("/")

    return render_template("create.html")

@app.route("/balance", methods=["GET", "POST"])
def balance():
    account = None
    if request.method == "POST":
        acc_no = int(request.form["acc_no"])
        data = load_data()

        for acc in data["accounts"]:
            if acc["acc_no"] == acc_no:
                account = acc
                break

    return render_template("balance.html", account=account)


@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if request.method == "POST":
        acc_no = int(request.form["acc_no"])
        amount = float(request.form["amount"])

        data = load_data()
        for acc in data["accounts"]:
            if acc["acc_no"] == acc_no:
                acc["balance"] += amount
                break

        save_data(data)
        return redirect("/")

    return render_template("deposit.html")


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    if request.method == "POST":
        acc_no = int(request.form["acc_no"])
        amount = float(request.form["amount"])

        data = load_data()
        for acc in data["accounts"]:
            if acc["acc_no"] == acc_no and acc["balance"] >= amount:
                acc["balance"] -= amount
                break

        save_data(data)
        return redirect("/")

    return render_template("withdraw.html")


@app.route("/accounts")
def accounts():
    data = load_data()
    return render_template("accounts.html", accounts=data["accounts"])


@app.route("/highest")
def highest():
    data = load_data()
    highest_acc = None

    if data["accounts"]:
        highest_acc = max(data["accounts"], key=lambda x: x["balance"])

    return render_template("highest.html", account=highest_acc)


if __name__ == "__main__":
    app.run(debug=True)
