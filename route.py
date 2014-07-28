import os
import flask
import db_connection

app = flask.Flask(__name__)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    db = db_connection.DbConnection()
    if flask.request.method == 'POST':
        subject_code = flask.request.form['subject_code']
        email = flask.request.form['email']
    else:
        subject_code = flask.request.args.get('subject_code')
        email = flask.request.args.get('email')
    db.insert_item(subject_code, email)
    return "Done"


@app.route('/query')
def query():
    db = db_connection.DbConnection()
    items = db.query_all()
    html = ["%s, %s" % (i['subject_code'], i['email']) for i in items]
    return '\n'.join(html)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', False))
