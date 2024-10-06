from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para obter a conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota para exibir a lista de tarefas
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Rota para adicionar uma nova tarefa
@app.route('/add', methods=('GET', 'POST'))
def add_task_route():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        responsible = request.form['responsible']
        due_date = request.form['due_date']

        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (title, description, priority, responsible, due_date, status) VALUES (?, ?, ?, ?, ?, ?)',
                    (title, description, priority, responsible, due_date, 'Pendente'))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

# Rota para editar uma tarefa existente
@app.route('/edit/<int:task_id>', methods=('GET', 'POST'))
def edit_task_route(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        responsible = request.form['responsible']
        due_date = request.form['due_date']

        conn.execute('UPDATE tasks SET title = ?, description = ?, priority = ?, responsible = ?, due_date = ? WHERE id = ?',
                    (title, description, priority, responsible, due_date, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', task=task)

# Rota para transferir uma tarefa
@app.route('/transfer/<int:task_id>', methods=('GET', 'POST'))
def transfer_task_route(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if request.method == 'POST':
        new_responsible = request.form['responsible']

        conn.execute('UPDATE tasks SET responsible = ? WHERE id = ?',
                    (new_responsible, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('transfer.html', task=task)

# Rota para excluir uma tarefa
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
