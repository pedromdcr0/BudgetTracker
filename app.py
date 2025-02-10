from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify
from models import db, Item
from datetime import datetime

app = Flask(__name__)

app.secret_key = "peanut"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    # Busca todos os itens no banco
    items = Item.query.all()
    
    # Passa os itens para o template
    return render_template('index.html', items=items)


@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json

    new_item = Item(
        type=data.get("type"),
        description=data.get("description"),
        tags=",".join(data.get("tags", [])),
        deadline=datetime.strptime(data.get("deadline"), "%Y-%m-%d") if data.get("deadline") else None,
        created_in=datetime.now(),
        category=data.get("category")
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Item adicionado com sucesso!", "id": new_item.id}), 201


if __name__ == '__main__':
    app.run(debug=True)