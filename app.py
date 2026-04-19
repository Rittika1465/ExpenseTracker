from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# Load data
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

transactions = load_data()

@app.route('/')
def home():
    return redirect('/form')


@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        t_type = request.form.get("type")
        date = request.form.get("date")
        notes = request.form.get("notes")

        transaction = {
            "id": len(transactions),
            "amount": amount,
            "category": category,
            "type": t_type,
            "date": date,
            "notes": notes
        }

        transactions.append(transaction)
        save_data(transactions)

        return redirect('/view')

    return render_template("form.html")


@app.route('/view')
def view():
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")

    return render_template(
        "view.html",
        transactions=transactions,
        income=total_income,
        expense=total_expense
    )


@app.route('/delete/<int:id>')
def delete(id):
    global transactions
    transactions = [t for t in transactions if t["id"] != id]
    save_data(transactions)
    return redirect('/view')


if __name__ == "__main__":
    app.run(debug=True)