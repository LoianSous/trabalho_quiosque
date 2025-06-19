
# Projeto Quiosque – Painel com Flask

Este projeto é um painel administrativo e de exibição de imagens feito com Flask. Permite upload de imagens, controle de exibição e gerenciamento de usuários via e-mail.

## Tecnologias utilizadas

- Python 3
- Flask
- Flask-Mail
- itsdangerous
- Werkzeug
- SQLite (nativo)

## Como executar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repositorio
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
# Ative o ambiente virtual:
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python app.py
```

> Acesse no navegador: [http://localhost:5000](http://localhost:5000)

---

## Configurações

Isso aqui server para que um email de alterar senha seja mandado quando um usuario é criado:

```python
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'sua_senha_app'
```
---

## Uploads

As imagens são armazenadas na pasta `static/uploads`. Ela será criada automaticamente se não existir.

## Para visualizar o banco de dados ou modifica-lo, acesse o powershell, vá até o local do projeto, e digite:

```bash
sqlite3 database.db
```
Assim vai abrir o banco de dados e vai aparecer:

 sqlite>

Depois digite .tables para visualizar as tabelas.

## Comandos git utilizados:

git branch - para ver em qual branch está.

git branch -r - para ver branchs remotas.

git init - inicia o git na pasta.

git remote add origin https://github.com/seu-usuario/nome-do-repositorio.git - para adicionar o repositorio do git no projeto.

git add .

git commit -m "Primeiro commit"

git push -u origin master ou main.

git checkout -b loian para criar uma nova branch.

git checkout nome_da_branch - para mudar de branch.

git merge loian - passa os arquivos da branch loian para main.