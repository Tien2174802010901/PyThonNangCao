import psycopg2
from psycopg2 import sql
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

DATABASE_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM moviedata')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        genres = request.form['genres']
        movie_id = request.form['id']
        original_language = request.form['original_language']
        release_date = request.form['release_date']
        runtime = request.form['runtime']
        title = request.form['title']
        vote_average = request.form['vote_average']
        director = request.form['director']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO moviedata (genres, id, original_language, release_date, runtime, title, vote_average, director) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (genres, movie_id, original_language, release_date, runtime, title, vote_average, director)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete', methods=['POST'])
def delete():
    movie_id = request.form['id']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM moviedata WHERE id = %s', (movie_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = []
    search_term = ""
    if request.method == 'POST':
        search_term = request.form['search_term']
        search_type = request.form['search_type']
        conn = get_db_connection()
        cur = conn.cursor()

        if search_type == 'title':
            query = sql.SQL("SELECT * FROM moviedata WHERE title ILIKE %s")
            cur.execute(query, (f'%{search_term}%',))
        elif search_type == 'id':
            query = sql.SQL("SELECT * FROM moviedata WHERE id::text ILIKE %s")
            cur.execute(query, (f'%{search_term}%',))

        data = cur.fetchall()
        cur.close()
        conn.close()


        resp = make_response(render_template('search.html', data=data, search_term=search_term, search_type=search_type))
        resp.set_cookie('last_search_term', search_term)
        resp.set_cookie('last_search_type', search_type)
        return resp

    last_search_term = request.cookies.get('last_search_term', '')
    last_search_type = request.cookies.get('last_search_type', 'title')

    return render_template('search.html', data=data, search_term=last_search_term, search_type=last_search_type)

@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        selected_data = request.form.getlist('selected')

        existing_data = request.cookies.get('selected_data', '')
        combined_data = list(set(existing_data.split(',') + selected_data))
        combined_data = [item for item in combined_data if item]
        resp = make_response(redirect(url_for('details')))
        resp.set_cookie('selected_data', ','.join(combined_data))
        return resp

    selected_data = request.cookies.get('selected_data', '').split(',')
    if selected_data == ['']:
        selected_data = []

    conn = get_db_connection()
    cur = conn.cursor()
    if selected_data:
        query = sql.SQL("SELECT * FROM moviedata WHERE id IN ({})").format(
            sql.SQL(', ').join(map(sql.Literal, selected_data))
        )
        cur.execute(query)
        data = cur.fetchall()
    else:
        data = []
    cur.close()
    conn.close()

    return render_template('details.html', data=data)

@app.route('/saved', methods=['GET', 'POST'])
def saved():
    if request.method == 'POST':
        
        if 'delete' in request.form:
            movie_id = request.form['id']
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM moviedata WHERE id = %s', (movie_id,))
            conn.commit()
            cur.close()
            conn.close()

            existing_data = request.cookies.get('selected_data', '').split(',')
            new_data = [item for item in existing_data if item != movie_id]

            resp = make_response(redirect(url_for('saved')))
            resp.set_cookie('selected_data', ','.join(new_data))
            return resp

        to_remove = request.form.getlist('selected')
        existing_data = request.cookies.get('selected_data', '').split(',')
        new_data = [item for item in existing_data if item not in to_remove and item]

        resp = make_response(redirect(url_for('saved')))
        resp.set_cookie('selected_data', ','.join(new_data))
        return resp

    selected_data = request.cookies.get('selected_data', '').split(',')
    if selected_data == ['']:
        selected_data = []

    conn = get_db_connection()
    cur = conn.cursor()
    if selected_data:
        query = sql.SQL("SELECT * FROM moviedata WHERE id IN ({})").format(
            sql.SQL(', ').join(map(sql.Literal, selected_data))
        )
        cur.execute(query)
        data = cur.fetchall()
    else:
        data = []

    cur.close()
    conn.close()

    return render_template('saved.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
