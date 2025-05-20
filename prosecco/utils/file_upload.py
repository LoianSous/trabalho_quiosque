from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

# Definição da tarefa agendada
def tarefa_agendada():
    print("Executando tarefa em segundo plano!")

# Configuração do agendador
app.config['SCHEDULER_API_ENABLED'] = True
scheduler.init_app(app)
scheduler.start()

# Adicionando uma tarefa que executa a cada 10 segundos
scheduler.add_job(id='Tarefa1', func=tarefa_agendada, trigger='interval', seconds=10)

@app.route('/')
def home():
    return "Flask-APScheduler está rodando!"

if __name__ == '__main__':
    app.run(debug=True)
