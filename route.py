import os
import flask
import db_connection
import re

app = flask.Flask(__name__)

subject_code_pattern = r"(?<=subject=)\d{16}(?=$)"
sec_pattern = r"^(\d\d,)*\d\d$|^\*$"
email_pattern = "(?i)^[\w._-]+?@[\w.-]+.\w+$"
re_subject_code = re.compile(subject_code_pattern)
re_sec_list = re.compile(sec_pattern)
re_email = re.compile(email_pattern)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    db = db_connection.DbConnection()
    if flask.request.method == 'POST':
        url = flask.request.form['url']
        email = flask.request.form['email']
        wanted_sec = flask.request.form['sec']
    else:
        url = flask.request.args.get('url')
        email = flask.request.args.get('email')
        wanted_sec = flask.request.args.get('sec')
    regex_result = re_subject_code.search(url)
    regex_email_match = re_email.match(email)
    regex_sec_match = re_sec_list.match(wanted_sec)
    result = "Failed:"
    if regex_result and regex_sec_match and regex_email_match:
        subject_code = regex_result.group()
        db.insert_item(subject_code, email, wanted_sec)
        result = "Done"
    else:
        fail_count = 0
        result = "Failed: "
        if not regex_result:
            result += "url"
            fail_count += 1
        if not regex_sec_match:
            if fail_count > 0:
                result += ", "
            result += "sec"
            fail_count += 1
        if not regex_email_match:
            if fail_count > 0:
                result += ", "
            result += "email"
        result += " wrong"
    return result


def display_items(items, date='date'):
    protected = lambda x: x[:4] + '*'*(len(x)-4) if len(x) >= 4 else ''
    if items:
        html = ["%s %s %s %s" % (i.get(date, ""), i.get('subject_code', ""),
                protected(i.get('email')), i.get('sec', '')) for i in items]
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
