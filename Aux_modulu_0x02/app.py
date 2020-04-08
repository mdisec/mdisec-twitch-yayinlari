import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://test:test@localhost:5432/test"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class LogModel(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String())
    user_agent = db.Column(db.String())
    create_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __init__(self, ip, user_agent):
        self.ip = ip
        self.user_agent = user_agent

    def __repr__(self):
        return f"<Log {self.ip}>"


def log_request(ip, user_agent):
    eng = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        with eng.connect() as con:
            query = "INSERT INTO logs (ip, user_agent) VALUES ('{0}','{1}')".format(
                ip,user_agent
            )
            con.execute(query)
    except Exception as e:
        pass

@app.route('/')
def hello_world():
    author = request.args.get('author')

    log_request(
        request.remote_addr,
        request.headers.get('User-Agent')
    )
    return "Helloooo {0} !".format(
        author
    )


if __name__ == '__main__':
    app.run()
