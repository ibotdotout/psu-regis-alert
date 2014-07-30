import os
import flask
import db_connection
import re

app = flask.Flask(__name__)
subject_code_pattern = r"(?<=subject=)\d*(?=$)"
re_subject_code = re.compile(subject_code_pattern)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    db = db_connection.DbConnection()
    if flask.request.method == 'POST':
        url = flask.request.form['url']
        email = flask.request.form['email']
    else:
        url = flask.request.args.get('url')
        email = flask.request.args.get('email')
    regex_result = re_subject_code.search(url)
    if regex_result:
        subject_code = regex_result.group()
        db.insert_item(subject_code, email)
        return "Done"
    else:
        return "Failed: Url Wrong"


def display_items(items, date='date'):
    if items:
        html = ["%s %s" % (i[date], i['subject_code']) for i in items]
        return '<br>'.join(html)
    else:
        return "Query Failed!!!"


@app.route('/queue')
def query_queue():
    db = db_connection.DbConnection()
    items = db.query_queue_all()
    return display_items(items)


@app.route('/used')
def query_used():
    db = db_connection.DbConnection()
    items = db.query_used_all()
    return display_items(items, 'achived_date')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', False))
