from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_migrate import Migrate
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://msf:msf@localhost:5432/msf"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class LogModel(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String())
    user_agent = db.Column(db.String())

    def __init__(self, ip, user_agent):
        self.ip = ip
        self.user_agent = user_agent

    def __repr__(self):
        return f"<Log {self.ip}>"

def log_kaydet(ip, user_agent):
    eng = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    with eng.connect() as con:
        query = "INSERT INTO logs (ip, user_agent) VALUES ('{0}','{1}')".format(
            ip,
            user_agent
        )
        con.execute(query)


@app.route('/')
def hello_world():

    log_kaydet(
        request.remote_addr,
        request.headers.get('user-agent')
    )

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
