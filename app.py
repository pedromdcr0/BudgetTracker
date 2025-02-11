from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify
from models import db, Item, Category
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
    items = Item.query.all()
    return render_template('index.html', items=items)


@app.route('/add_item', methods=['POST'])
def add_item():
    categoria = Category.query.filter_by(name=request.form['category']).first()

    if not categoria:
        categoria = Category(name = request.form['category'])
        db.session.add(categoria)
        db.session.flush()

    new_item = Item(
        type = request.form['type'],
        description = request.form['description'],
        value = float(request.form['value'].replace(',', '.')),
        tags = "",
        deadline = datetime.strptime(request.form['deadline'], "%Y-%m-%d"),
        created_in = datetime.now(),
        category_id = categoria.id
    )

    db.session.add(new_item)
    db.session.commit()

    return redirect('/')


@app.route('/buscar-categorias', methods=['GET'])
def buscar_categorias():
    query = request.args.get('query', '')
    categorias = Category.query.filter(Category.name.ilike(f'%{query}%')).all()   
    return jsonify({'categories': [{'id': categoria.id, 'name': categoria.name} for categoria in categorias]})


@app.route('/add_test_item')
def add_test_item():
    categoria = Category.query.filter_by(name='Categoria Teste').first()
    if not categoria:
        categoria = Category(name='Categoria Teste')
        db.session.add(categoria)
        db.session.commit()

    item_teste = Item(
        type='Teste',
        description='Este é um item de teste.',
        tags='teste, exemplo',
        deadline = datetime.now(),
        created_in = datetime.now(),
        category_id = categoria.id
    )
    db.session.add(item_teste)
    db.session.commit()

    return 'Item de teste adicionado com sucesso!'


@app.route('/criar-categoria', methods=['POST'])
def criar_categoria():
    data = request.json
    nome_categoria = data.get('name')
    
    categoria_existente = Category.query.filter_by(name=nome_categoria).first()
    
    if categoria_existente:
        return jsonify({'success': False, 'message': 'Categoria já existe'}), 400
    
    nova_categoria = Category(name=nome_categoria)
    db.session.add(nova_categoria)
    db.session.commit()
    
    return jsonify({'success': True, 'category': {'id': nova_categoria.id, 'name': nova_categoria.name}}), 201



if __name__ == '__main__':
    app.run(debug=True)