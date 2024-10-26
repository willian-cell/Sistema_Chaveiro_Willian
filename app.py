from flask import Flask, render_template_string, request, redirect, flash
import sqlite3

# Configuração da aplicação Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

DB_NAME = 'financeiro.db'

# Criação do banco de dados
def criar_banco():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            unidade INTEGER,
            valor_unitario REAL,
            valor_total REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL
        )
    ''')
    conexao.commit()
    conexao.close()

# Função para inserir uma nova venda
def inserir_venda(data, descricao, unidade, valor_unitario):
    valor_total = unidade * valor_unitario
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO vendas (data, descricao, unidade, valor_unitario, valor_total) VALUES (?, ?, ?, ?, ?)',
                   (data, descricao, unidade, valor_unitario, valor_total))
    conexao.commit()
    conexao.close()


# Função para listar todas as vendas
def listar_vendas():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    conexao.close()
    return vendas


@app.route('/')
def index():
    vendas = listar_vendas()
    return render_template_string(TEMPLATE, vendas=vendas)


@app.route('/vendas', methods=['POST'])
def cadastrar_venda():
    data = request.form['data']
    descricao = request.form['descricao']
    unidade = int(request.form['unidade'])
    valor_unitario = float(request.form['valor_unitario'])
    inserir_venda(data, descricao, unidade, valor_unitario)
    flash('Venda cadastrada com sucesso!')
    return redirect('/')

# Template HTML com Bootstrap embutido
TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema SaaS de Vendas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <style>
        body { background-color: #1c1c1c; color: white; font-family: 'Arial', sans-serif; }
        .navbar { background-color: #343a40; }
        .card { background-color: #2c2c2c; margin-top: 20px; }
        .btn-primary { background-color: #0d6efd; border: none; transition: transform 0.3s ease; }
        .btn-primary:hover { background-color: #0a58ca; transform: scale(1.05); }
        .list-group-item { background-color: #1f1f1f; color: white; }
        footer { background-color: #343a40; padding: 10px; text-align: center; color: #aaa; margin-top: auto; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">Sistema SaaS de Vendas</a>
        </div>
    </nav>

    <div class="container mt-5">
        <h1 class="text-center mb-5">Gestão Financeira</h1>

        <div class="row">
            <div class="col-md-6">
                <div class="card p-4">
                    <h3 class="text-center">Cadastrar Venda</h3>
                    <form method="POST" action="/vendas" onsubmit="return validarFormulario()">
                        <div class="mb-3">
                            <label for="data" class="form-label">Data</label>
                            <input type="date" class="form-control" id="data" name="data" required>
                        </div>
                        <div class="mb-3">
                            <label for="descricao" class="form-label">Descrição</label>
                            <input type="text" class="form-control" id="descricao" name="descricao" required>
                        </div>
                        <div class="mb-3">
                            <label for="unidade" class="form-label">Unidade</label>
                            <input type="number" class="form-control" id="unidade" name="unidade" min="1" required>
                        </div>
                        <div class="mb-3">
                            <label for="valor_unitario" class="form-label">Valor Unitário</label>
                            <input type="number" step="0.01" class="form-control" id="valor_unitario" name="valor_unitario" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Cadastrar</button>
                    </form>
                </div>
            </div>
        </div>

        <div class="card p-3 mt-5">
            <h3>Vendas Registradas</h3>
            <ul class="list-group mt-3">
                {% for venda in vendas %}
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>{{ venda[1] }} - {{ venda[2] }}</span>
                    <span class="badge bg-primary rounded-pill">R$ {{ venda[5] }}</span>
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 - Sistema SaaS de Vendas | Desenvolvido com Bootstrap e Flask</p>
    </footer>

    <script>
        function validarFormulario() {
            const unidade = document.getElementById('unidade').value;
            const valorUnitario = document.getElementById('valor_unitario').value;

            if (unidade <= 0) {
                alert('A unidade deve ser maior que 0.');
                return false;
            }
            if (valorUnitario <= 0) {
                alert('O valor unitário deve ser maior que 0.');
                return false;
            }
            return true;
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True)
