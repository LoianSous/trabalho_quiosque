from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def painel():
    return render_template('painel_exibicao.html')

@app.route('/login')
def login():
    return render_template('painel_login.html')

@app.route('/adm')
def adm():
    return render_template('painel_adm.html')

if __name__ == '__main__':
    app.run(debug=True)
