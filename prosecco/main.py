from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv('.env')

prosecco = Flask(__name__)

prosecco.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

@prosecco.route('/')
def hello():
    return 'just a test'


if __name__ == '__main__':
    prosecco.run(debug=True)