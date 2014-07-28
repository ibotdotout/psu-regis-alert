import os
import flask
import db_connection

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    db = db_connection.DbConnection()
    subject_code = flask.request.form['code']
    email = flask.request.form['email']
    return db.insert(subject_code, email)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', False))
