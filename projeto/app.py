from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from collections import defaultdict
import os
import sqlite3

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[] 
)
app.secret_key = 'uma_chave_secreta_segura_aqui'
app.permanent_session_lifetime = timedelta(minutes=10)  

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'loian9109@gmail.com'  
app.config['MAIL_PASSWORD'] = 'dfbkqfcwnviccvrm'     
app.config['MAIL_DEFAULT_SENDER'] = 'loian9109@gmail.com'

mail = Mail(app)

tentativas_por_email = defaultdict(list)

s = URLSafeTimedSerializer(app.secret_key)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['DATABASE'] = 'database.db'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def enviar_email(destinatario, assunto, corpo):
    msg = Message(
        subject=assunto,
        recipients=[destinatario],
        body=corpo
    )
    mail.send(msg)

@app.before_request
def verificar_expiracao_sessao():
    if 'user_id' in session:
        session.modified = True  
    elif request.endpoint in ['adm', 'upload', 'cadastrar_tela', 'criar_usuario', 'atualizar_tipo_usuario',
                              'deletar_usuario', 'reenviar_senha']:
        flash('Sua sessão expirou. Faça login novamente.', 'warning')
        return redirect(url_for('login'))

@app.route('/check_new_images/<identificador>')
def check_new_images(identificador):
    conn = get_db_connection()

    tela = conn.execute('SELECT id FROM telas WHERE identificador = ?', (identificador,)).fetchone()
    if tela:
        imagens = conn.execute(
            'SELECT filename FROM imagens WHERE tela_id = ? ORDER BY id DESC',
            (tela['id'],)
        ).fetchall()
    else:
        imagens = []

    total = len(imagens)
    ultima = imagens[0]['filename'] if imagens else None
    conn.close()
    
    return jsonify({
        'ultimaImagem': ultima,
        'totalImagens': total
    })

@app.route('/')
def painel():
    conn = get_db_connection()
    tela = conn.execute('SELECT id FROM telas WHERE identificador = ?', ('principal',)).fetchone()
    imagens = []
    if tela:
        imagens = conn.execute(
            'SELECT filename FROM imagens WHERE tela_id = ? ORDER BY id DESC',
            (tela['id'],)
        ).fetchall()
    conn.close()
    return render_template('painel_exibicao.html', imagens=imagens)


@limiter.limit("5 per minute")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:
            # ✅ Verifica se a conta está desativada
            if user['ativo'] == 0:
                flash("Esta conta está desativada. Contate o administrador.", "danger")
                conn.close()
                return redirect(url_for('login'))

            bloqueado_until = user['bloqueado_until']
            tentativas = user['tentativas_login']

            if bloqueado_until:
                bloqueado_dt = datetime.strptime(bloqueado_until, "%Y-%m-%d %H:%M:%S")
                if datetime.utcnow() < bloqueado_dt:
                    minutos = int((bloqueado_dt - datetime.utcnow()).total_seconds() // 60) + 1
                    flash(f'Conta bloqueada por muitas tentativas. Tente novamente em {minutos} minutos.', 'danger')
                    conn.close()
                    return redirect(url_for('login'))

            if check_password_hash(user['senha'], senha):
                # Login correto: resetar tentativas e bloqueio
                conn.execute('UPDATE users SET tentativas_login = 0, bloqueado_until = NULL WHERE id = ?', (user['id'],))
                conn.commit()
                conn.close()

                session.permanent = True
                session['user_id'] = user['id']
                session['email'] = user['email']
                flash('Logado com sucesso!', 'success')
                return redirect(url_for('adm'))
            else:
                # Incrementa tentativas
                tentativas += 1
                if tentativas >= 5:
                    bloqueado_novo = (datetime.utcnow() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
                    conn.execute('UPDATE users SET tentativas_login = ?, bloqueado_until = ? WHERE id = ?', (tentativas, bloqueado_novo, user['id']))
                    conn.commit()

                    # Enviar e-mail de alerta
                    corpo = f"""Olá!

Detectamos 5 tentativas de login malsucedidas na sua conta do Painel Administrativo IFMS ({email}).

Se não foi você, recomendamos alterar sua senha imediatamente.

Atenciosamente,
Painel IFMS
"""
                    try:
                        enviar_email(email, "Alerta de Tentativas de Login", corpo)
                    except:
                        pass

                    flash("Muitas tentativas incorretas. Conta bloqueada por 5 minutos.", "danger")
                else:
                    conn.execute('UPDATE users SET tentativas_login = ? WHERE id = ?', (tentativas, user['id']))
                    conn.commit()
                    flash("Email ou senha incorretos.", "danger")
                conn.close()
                return redirect(url_for('login'))

        else:
            conn.close()
            flash("Email ou senha incorretos.", "danger")
            return redirect(url_for('login'))

    return render_template('painel_login.html')

@app.route('/alterar_status_usuario/<int:id>', methods=['POST'])
def alterar_status_usuario(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if id == session['user_id']:
        flash('Você não pode desativar sua própria conta enquanto estiver logado.', 'warning')
        return redirect(url_for('adm', secao='gerenciar'))

    senha_digitada = request.form.get('senha_confirmacao')
    conn = get_db_connection()
    user_logado = conn.execute('SELECT senha FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    if not user_logado or not check_password_hash(user_logado['senha'], senha_digitada):
        conn.close()
        flash('Senha incorreta. Operação cancelada.', 'danger')
        return redirect(url_for('adm', secao='gerenciar'))

    novo_status = int(request.form['ativo'])
    conn.execute('UPDATE users SET ativo = ? WHERE id = ?', (novo_status, id))
    conn.commit()
    conn.close()
    flash('Status do usuário atualizado.', 'success')
    return redirect(url_for('adm', secao='gerenciar'))

@app.route('/adm')
def adm():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    secao = request.args.get('secao', default='inicio')
    conn = get_db_connection()

    telas = conn.execute('SELECT * FROM telas').fetchall()

    tela_principal = conn.execute("SELECT id FROM telas WHERE identificador = 'principal'").fetchone()
    id_tela_principal = tela_principal['id'] if tela_principal else None

    imagens_por_tela = {}
    telas_com_imagens = []

    for tela in telas:
        imagens = conn.execute('SELECT * FROM imagens WHERE tela_id = ?', (tela['id'],)).fetchall()
        imagens_por_tela[tela['id']] = imagens
        if imagens:
            telas_com_imagens.append(tela)

    imagens_tela_principal = []
    if id_tela_principal:
        imagens_tela_principal = conn.execute(
            'SELECT * FROM imagens WHERE tela_id = ?', (id_tela_principal,)
        ).fetchall()

    imagens_sem_tela = conn.execute('SELECT * FROM imagens WHERE tela_id IS NULL').fetchall()

    user = conn.execute('SELECT tipo FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    total_imagens = conn.execute('SELECT COUNT(*) as total FROM imagens').fetchone()['total']
    total_em_exibicao = sum(len(imagens) for imagens in imagens_por_tela.values()) + len(imagens_tela_principal)

    usuarios = conn.execute('SELECT id, email, tipo, ativo FROM users').fetchall()

    conn.close()

    return render_template('painel_adm.html',
                           telas=telas,
                           imagens_por_tela=imagens_por_tela,
                           imagens_tela_principal=imagens_tela_principal,
                           imagens_sem_tela=imagens_sem_tela,
                           telas_com_imagens=telas_com_imagens,
                           total_imagens=total_imagens,
                           total_em_exibicao=total_em_exibicao,
                           tipo_usuario=user['tipo'],
                           usuarios=usuarios,
                           secao=secao)

@app.route('/cadastrar_tela', methods=['POST'])
def cadastrar_tela():
    nome = request.form['nome']
    identificador = request.form['identificador']

    conn = get_db_connection()
    conn.execute('INSERT INTO telas (nome, identificador) VALUES (?, ?)', (nome, identificador))
    conn.commit()
    conn.close()

    flash('Tela cadastrada com sucesso!', 'success')
    return redirect(url_for('adm', secao='identificar'))

@app.route('/upload', methods=['POST'])
def upload():
    if 'imagem' not in request.files:
        return 'Nenhum arquivo enviado', 400

    imagem = request.files['imagem']
    if imagem.filename == '':
        return 'Nome de arquivo vazio', 400

    filename = secure_filename(imagem.filename)
    imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    tela_id_str = request.form.get('tela_id')
    tela_id = int(tela_id_str) if tela_id_str else None

    conn = get_db_connection()
    conn.execute('INSERT INTO imagens (filename, tela_id) VALUES (?, ?)', (filename, tela_id))
    conn.commit()
    conn.close()

    flash('Imagem enviada com sucesso!', 'success')
    return redirect(url_for('adm', secao='upload'))

@app.route('/exibicao/<identificador>')
def painel_exibicao_por_tela(identificador):
    conn = get_db_connection()
    tela = conn.execute('SELECT id FROM telas WHERE identificador = ?', (identificador,)).fetchone()
    imagens = []
    if tela:
        imagens = conn.execute('SELECT filename FROM imagens WHERE tela_id = ?', (tela['id'],)).fetchall()
    conn.close()
    return render_template('painel_exibicao.html', imagens=imagens)

@app.route('/delete_image/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    senha_digitada = request.form.get('senha_confirmacao', '').strip()
    conn = get_db_connection()
    
    usuario = conn.execute('SELECT senha FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not usuario or not check_password_hash(usuario['senha'], senha_digitada):
        flash('Senha incorreta. A imagem não foi removida.', 'danger')
        conn.close()
        return redirect(url_for('adm', secao='selecionar'))

    img = conn.execute('SELECT filename FROM imagens WHERE id = ?', (image_id,)).fetchone()
    if img:
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], img['filename'])
        if os.path.exists(caminho):
            os.remove(caminho)

        conn.execute('DELETE FROM imagens WHERE id = ?', (image_id,))
        conn.commit()
        flash('Imagem removida com sucesso!', 'success')
    else:
        flash('Imagem não encontrada.', 'danger')

    conn.close()
    return redirect(url_for('adm', secao='selecionar'))

@app.route('/delete_multiple_images', methods=['POST'])
def delete_multiple_images():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    senha_digitada = request.form.get('senha_confirmacao', '').strip()
    ids = request.form.getlist("ids[]")

    if not ids or ids == ['']:
        flash('Nenhuma imagem selecionada.', 'warning')
        return redirect(url_for('adm', secao='selecionar'))

    conn = get_db_connection()
    usuario = conn.execute('SELECT senha FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    if not usuario or not check_password_hash(usuario['senha'], senha_digitada):
        conn.close()
        flash('Senha incorreta. As imagens não foram removidas.', 'danger')
        return redirect(url_for('adm', secao='selecionar'))

    removidas = 0
    for image_id in ids:
        img = conn.execute('SELECT filename FROM imagens WHERE id = ?', (image_id,)).fetchone()
        if img:
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], img['filename'])
            if os.path.exists(caminho):
                os.remove(caminho)
            conn.execute('DELETE FROM imagens WHERE id = ?', (image_id,))
            removidas += 1

    conn.commit()
    conn.close()

    flash(f'{removidas} imagem(ns) removida(s) com sucesso!', 'success')
    return redirect(url_for('adm', secao='selecionar'))

@app.route('/remover_da_tela/<int:image_id>', methods=['POST'])
def remover_da_tela(image_id):
    conn = get_db_connection()
    conn.execute('UPDATE imagens SET tela_id = NULL WHERE id = ?', (image_id,))
    conn.commit()
    conn.close()
    flash('Imagem removida da tela, mas mantida no banco de dados.', 'info')
    return redirect(url_for('adm', secao='upload'))

@app.route('/atribuir_tela', methods=['POST'])
def atribuir_tela():
    imagem_id = request.form.get('imagem_id')
    tela_id = request.form.get('tela_id')

    if imagem_id and tela_id:
        conn = get_db_connection()
        conn.execute('UPDATE imagens SET tela_id = ? WHERE id = ?', (tela_id, imagem_id))
        conn.commit()
        conn.close()
        flash('Imagem atribuída à nova tela com sucesso!', 'success')
    else:
        flash('Erro ao atribuir tela. Dados incompletos.', 'danger')

    return redirect(url_for('adm', secao='selecionar'))

@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    nome = request.form['nome']
    email = request.form['email']
    tipo = request.form['tipo']

    senha_padrao = 'ifms123'
    senha_hash = generate_password_hash(senha_padrao)

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (email, senha, tipo) VALUES (?, ?, ?)', (email, senha_hash, tipo))
        conn.commit()
        conn.execute('UPDATE users SET token_usado = 0 WHERE email = ?', (email,))
        conn.commit()
        flash('Usuário criado com sucesso!', 'success')

        token = s.dumps(email, salt='redefinir-senha')
        link = url_for('alterar_senha', token=token, _external=True)

        msg = Message('Redefinir sua senha - IFMS', recipients=[email])
        msg.body = f"""
Olá, {nome}!

Sua conta no painel do IFMS foi criada.

Para definir sua senha pessoal e substituir a senha padrão, clique no link abaixo:

{link}

Este link expira em 1 hora por segurança.

Atenciosamente,
Painel IFMS
"""
        mail.send(msg)

    except sqlite3.IntegrityError:
        flash('Erro: este email já está cadastrado.', 'danger')
    finally:
        conn.close()

    return redirect(url_for('adm', secao='gerenciar'))

@app.route('/atualizar_tipo_usuario/<int:id>', methods=['POST'])
def atualizar_tipo_usuario(id):
    novo_tipo = request.form['tipo']
    conn = get_db_connection()
    conn.execute('UPDATE users SET tipo = ? WHERE id = ?', (novo_tipo, id))
    conn.commit()
    conn.close()
    flash('Tipo de usuário atualizado.', 'success')
    return redirect(url_for('adm', secao='gerenciar'))

@app.route('/deletar_usuario/<int:id>', methods=['POST'])
def deletar_usuario(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if id == session['user_id']:
        flash('Você não pode excluir sua própria conta enquanto estiver logado.', 'warning')
        return redirect(url_for('adm', secao='gerenciar'))

    senha_digitada = request.form.get('senha_confirmacao')
    conn = get_db_connection()
    user_logado = conn.execute('SELECT senha FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    if not user_logado or not check_password_hash(user_logado['senha'], senha_digitada):
        conn.close()
        flash('Senha incorreta. Operação cancelada.', 'danger')
        return redirect(url_for('adm', secao='gerenciar'))

    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Usuário removido com sucesso!', 'success')
    return redirect(url_for('adm', secao='gerenciar'))

@app.route('/reenviar_senha/<int:id>', methods=['POST'])
def reenviar_senha(id):
    conn = get_db_connection()
    user = conn.execute('SELECT email FROM users WHERE id = ?', (id,)).fetchone()

    if user:
        email = user['email']
        conn.execute('UPDATE users SET token_usado = 0 WHERE id = ?', (id,))
        conn.commit()

        token = s.dumps(email, salt='redefinir-senha')
        link = url_for('alterar_senha', token=token, _external=True)

        msg = Message('Redefinir sua senha - IFMS', recipients=[email])
        msg.body = f"""
Olá!

Você solicitou uma redefinição de senha.

Clique no link abaixo para definir uma nova senha:

{link}

Este link expira em 1 hora por segurança.

Atenciosamente,
Painel IFMS
"""
        mail.send(msg)
        flash('Link de redefinição enviado.', 'success')
    else:
        flash('Usuário não encontrado.', 'danger')

    return redirect(url_for('adm', secao='gerenciar'))

@app.route('/alterar_senha/<token>', methods=['GET', 'POST'])
def alterar_senha(token):
    try:
        email = s.loads(token, salt='redefinir-senha', max_age=3600)
    except:
        flash('Link expirado ou inválido.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT token_usado FROM users WHERE email = ?', (email,)).fetchone()

    if user is None:
        conn.close()
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('login'))

    if user['token_usado']:
        conn.close()
        flash('Este link já foi utilizado.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        hash_senha = generate_password_hash(nova_senha)

        conn.execute('UPDATE users SET senha = ?, token_usado = 1 WHERE email = ?', (hash_senha, email))
        conn.commit()
        conn.close()

        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('login'))

    conn.close()
    return render_template('redefinir_senha.html', email=email)


@app.route('/logout')
def logout():
    session.clear()
    flash('Deslogado com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)