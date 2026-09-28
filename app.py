from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/')
def index():
    connection = get_db_connection()

    contents = connection.execute(
        '''
        SELECT id, name, category, photo
        FROM product
        WHERE status = 'on'
        ORDER BY created_at DESC
        '''
    ).fetchall()

    connection.close()

    total = len(contents)

    return render_template(
        'index.html',
        contents=contents,
        total=total
    )


@app.route('/new', methods=['GET', 'POST'])
def new():

    if request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        photo = request.form['photo']

        connection = get_db_connection()

        connection.execute(
            '''
            INSERT INTO product
            (name, description, category, photo)
            VALUES (?, ?, ?, ?)
            ''',
            (
                name,
                description,
                category,
                photo
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for('index'))

    return render_template('new.html')


@app.route('/view/<int:id>')
def view(id):

    connection = get_db_connection()

    product = connection.execute(
        '''
        SELECT *
        FROM product
        WHERE id = ?
        AND status != 'del'
        ''',
        (id,)
    ).fetchone()

    connection.close()

    return render_template(
        'view.html',
        product=product
    )


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    connection = get_db_connection()

    product = connection.execute(
        '''
        SELECT *
        FROM product
        WHERE id = ?
        AND status != 'del'
        ''',
        (id,)
    ).fetchone()


    if request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        photo = request.form['photo']
        status = request.form['status']

        connection.execute(
            '''
            UPDATE product
            SET
                name = ?,
                description = ?,
                category = ?,
                photo = ?,
                status = ?
            WHERE id = ?
            ''',
            (
                name,
                description,
                category,
                photo,
                status,
                id
            )
        )

        connection.commit()
        connection.close()

        return redirect(
            url_for('view', id=id)
        )

    connection.close()

    return render_template(
        'edit.html',
        product=product
    )


@app.route('/delete/<int:id>')
def delete(id):

    connection = get_db_connection()

    connection.execute(
        '''
        UPDATE product
        SET status = 'del'
        WHERE id = ?
        ''',
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for('index')
    )


@app.route('/about')
def about():

    return render_template(
        'about.html'
    )


if __name__ == '__main__':
    app.run(debug=True)

    