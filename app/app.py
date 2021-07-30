from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'namedb'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'SaiK'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, persons=result)


@app.route('/view/<int:person_id>', methods=['GET'])
def record_view(person_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details WHERE id=%s', person_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', person=result[0])


@app.route('/edit/<int:person_id>', methods=['GET'])
def form_edit_get(person_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details WHERE id=%s', person_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', person=result[0])


@app.route('/edit/<int:person_id>', methods=['POST'])
def form_update_post(person_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('first_name'), request.form.get('last_name'), request.form.get('company_name'),
                 request.form.get('address'), request.form.get('phone'), person_id)
    sql_update_query = """UPDATE details d SET d.first_name = %s, d.last_name = %s, d.company_name = %s, d.address = %s, 
                        d.phone = %s WHERE d.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/person/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Person Form')


@app.route('/person/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('first_name'), request.form.get('last_name'), request.form.get('company_name'),
                 request.form.get('address'), request.form.get('phone'))
    sql_insert_query = """INSERT INTO details (first_name,last_name, company_name, address, phone) 
                VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:person_id>', methods=['POST'])
def form_delete_post(person_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM details WHERE id = %s """
    cursor.execute(sql_delete_query, person_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/people', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:person_id>', methods=['GET'])
def api_retrieve(person_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details WHERE id=%s', person_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:person_id>', methods=['PUT'])
def api_edit(person_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/people/<int:person_id>', methods=['DELETE'])
def api_delete(person_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
