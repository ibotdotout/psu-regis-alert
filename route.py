import os
import flask
import db_connection
import re
import collections
import datetime
from flask.ext.compress import Compress

app = flask.Flask(__name__)
Compress(app)

subject_code_pattern = r"(?<=subject=)\d{16}(?=$)"
sec_pattern = r"^(\d\d,)*\d\d$|^\*$"
email_pattern = "(?i)^[\w._-]+?@[\w.-]+.\w+$"
re_subject_code = re.compile(subject_code_pattern)
re_sec_list = re.compile(sec_pattern)
re_email = re.compile(email_pattern)


def get_parametes(request):
    if request.method == 'POST':
        form = request.form
    else:
        form = request.args

    param_names = ['url', 'email', 'sec', 'line_id']
    Params = collections.namedtuple('Params', param_names)
    params = Params._make([form.get(name) for name in param_names])
    return params


def verify_parmas(params):
    regex_result = re_subject_code.search(params.url)
    regex_email_match = re_email.match(params.email)
    regex_sec_match = re_sec_list.match(params.sec)

    return [regex_result, regex_sec_match,
            regex_email_match or params.line_id]


def _insert_to_db(params):
    db = db_connection.DbConnection()
    regex_result = re_subject_code.search(params.url)
    subject_code = regex_result.group()
    url = params.url
    avoid_keyword = ("/Student/", "/Search/")
    for keyword in avoid_keyword:
        url = url.replace(keyword, "/")
    line_id = params.line_id if params.line_id else ""
    db.insert_item(url, subject_code, params.email,
                   line_id, params.sec)


def display_items(items, date='date'):

    def protected(x, is_protect=True):
        if is_protect:
            x = x[:4] + '*' * (len(x) - 4) if len(x) >= 4 else ''
        return x

    def line_template(item, date):
        def convert_to_str(val):
            return str(val) if isinstance(
                val,
                datetime.datetime) else val.encode('utf-8').strip()

        names = [date, 'subject_code', 'sec', 'email', 'line_id']
        protect_list = [False, False, False, True, True]
        values = [convert_to_str(item.get(name, "")) for name in names]
        values = [protected(val, is_protect)
                  for val, is_protect in zip(values, protect_list)]
        return " ".join(values)

    display = "Query Failed!!!"

    if items:
        html = [line_template(i, date) for i in items]
        display = '<br>'.join(html)

    return display


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    params = get_parametes(flask.request)
    verify_results = verify_parmas(params)

    if all(verify_results):
        _insert_to_db(params)
        result = "Done"
    else:
        names = ["url", "sec", "email or line_id"]
        error_msg = [name for i, name in zip(verify_results, names) if not i]
        result = "Failed: " + ",".join(error_msg) + " wrong"

    return result


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
    debug = True if os.environ.get('DEBUG', "False") == "True" else False
    app.run(host='0.0.0.0', port=port, debug=debug)
