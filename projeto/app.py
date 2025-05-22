from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['DATABASE'] = 'database.db'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def painel():
    conn = get_db_connection()
    imagens = conn.execute('SELECT filename FROM imagens').fetchall()
    conn.close()
    return render_template('painel_exibicao.html', imagens=imagens)

@app.route('/login')
def login():
    return render_template('painel_login.html')

@app.route('/adm')
def adm():
    conn = get_db_connection()
    imagens = conn.execute('SELECT * FROM imagens').fetchall()
    conn.close()
    return render_template('painel_adm.html', imagens=imagens)

@app.route('/upload', methods=['POST'])
def upload():
    if 'imagem' not in request.files:
        return 'Nenhum arquivo enviado', 400

    imagem = request.files['imagem']
    if imagem.filename == '':
        return 'Nome de arquivo vazio', 400

    filename = secure_filename(imagem.filename)
    imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db_connection()
    conn.execute('INSERT INTO imagens (filename) VALUES (?)', (filename,))
    conn.commit()
    conn.close()

    return redirect(url_for('adm')) 

@app.route('/delete_image/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    conn = get_db_connection()
    img = conn.execute('SELECT filename FROM imagens WHERE id = ?', (image_id,)).fetchone()

    if img:
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], img['filename'])
        if os.path.exists(caminho):
            os.remove(caminho) 

        conn.execute('DELETE FROM imagens WHERE id = ?', (image_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('adm'))


if __name__ == '__main__':
    app.run(debug=True)