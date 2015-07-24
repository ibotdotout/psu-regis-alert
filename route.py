import os
import flask
import db_connection
import re
import collections

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
    db.insert_item(subject_code, params.email, params.line_id, params.sec)


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


def display_items(items, date='date'):
    def protected(x):
        return x[:4] + '*' * (len(x) - 4) if len(x) >= 4 else ''

    if items:
        html = [
            "%s %s %s %s" %
            (i.get(
                date, ""), i.get(
                'subject_code', ""), protected(
                i.get('email')), i.get(
                    'sec', '')) for i in items]
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
