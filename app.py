from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def format_date(date_string):
    """Converte uma string de data para o formato brasileiro (DD/MM/AAAA)."""
    if date_string:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")  # Formato original YYYY-MM-DD
        return date_object.strftime("%d/%m/%Y")
    return ""

def format_datetime(datetime_string):
    """Converte uma string de data e hora para o formato brasileiro (DD/MM/AAAA HH:MM)."""
    if datetime_string:
        datetime_object = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")  # Formato original YYYY-MM-DD HH:MM:SS
        return datetime_object.strftime("%d/%m/%Y %H:%M")
    return ""

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()

    # Formatar as datas
    formatted_tasks = []
    for task in tasks:
        task_dict = dict(task)  # Converte o Row em um dicionário
        task_dict['due_date'] = format_date(task_dict['due_date'])  # Formatar data de conclusão
        if task_dict['completed_at']:
            task_dict['completed_at'] = format_datetime(task_dict['completed_at'])  # Formatar data e hora de conclusão
        formatted_tasks.append(task_dict)

    return render_template('index.html', tasks=formatted_tasks)

@app.route('/add', methods=['GET', 'POST'])
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

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
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

    return render_template('edit.html', task=task)

@app.route('/transfer/<int:task_id>', methods=['GET', 'POST'])
def transfer_task_route(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if request.method == 'POST':
        new_responsible = request.form['responsible']
        conn.execute('UPDATE tasks SET responsible = ? WHERE id = ?', (new_responsible, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('transfer.html', task=task)

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    completed_by = request.form['completed_by']
    completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Registrar data e hora atual

    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status = ?, completed_by = ?, completed_at = ? WHERE id = ?',
                 ('Concluída', completed_by, completed_at, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
