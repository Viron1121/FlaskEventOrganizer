import sqlite3
from unicodedata import category
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import hashlib
import os

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM reservation WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_post_package(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM packages WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post




app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'



@app.route('/index')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM reservation').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)








    






@app.route('/')
def showpackages():
    
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM packages').fetchall()
    conn.close()
    return render_template('draft.html', posts=posts)



    


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/registration', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']

        if not fullname:
            flash('Fullname is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)',
                         (fullname, username, password))
            conn.commit()
            conn.close()


    return render_template('registration.html')



@app.route('/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        fullname = request.form['fullname']
        address = request.form['address']
        contact = request.form['contact']
        emailaddress = request.form['emailaddress']
        age = request.form['age']
        sex = request.form['sex']
        category = request.form['category']
        date = request.form['date']
        time = request.form['time']
        package = request.form['package']


        if not fullname:
            flash('Fullname is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO reservation (fullname, address, contact, emailaddress, age, sex, category, date, time,package) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?)',
                         (fullname, address, contact, emailaddress, age, sex, category, date, time,package))
            conn.commit()
            flash('Success!')
            conn.close()

    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM packages').fetchall()
    conn.close()
    
    return render_template('draft.html', posts=posts)



@app.route('/index', methods=('GET', 'POST'))
def package():    
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM reservation').fetchall()
    conn.close()
    
    return render_template('index.html', posts=posts)



app.config['UPLOAD_FOLDER']="static/images"
@app.route('/addpackage', methods=('GET', 'POST'))
def addpackage():
    if request.method == 'POST':
        packagename = request.form['packagename']
        description = request.form['description']
        price = request.form['price']
        person = request.form['person']
        food = request.form['food']
        upload_image=request.files['upload_image']

        

        if not packagename:
            flash('Package Name is required!')
        else:
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
            upload_image.save(filepath)
            conn = get_db_connection()
            cur=conn.cursor()
            cur.execute('INSERT INTO packages (packagename, description, price, person, food,img) VALUES (?, ?, ?, ?, ?,?)',
                         (packagename, description, price, person, food,upload_image.filename,))
            conn.commit()
            flash('Success!')
            conn.close()

    return render_template('addpackage.html')

@app.route('/viewpackage', methods=('GET', 'POST'))
def viewpackage():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM packages').fetchall()
    conn.close()
    return render_template('viewpackage.html', posts=posts)









@app.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM reservation WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['fullname']))
    return redirect(url_for('index'))

@app.route('/<int:id>/deletepackage', methods=('GET', 'POST'))
def deletepackage(id):
    post = get_post_package(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM packages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['packagename']))
    return redirect(url_for('viewpackage'))





@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        fullname = request.form['fullname']
        address = request.form['address']
        contact = request.form['contact']
        emailaddress = request.form['emailaddress']
        date = request.form['date']
        time = request.form['time']
        status = request.form['status']
        

        if not contact:
            flash('Contact number is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE reservation SET fullname = ?, address = ?, contact = ?, emailaddress = ?, date = ?, time = ?, status = ?'
                         ' WHERE id = ?',
                         (fullname, address,contact,emailaddress,date,time,status,id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM packages').fetchall()
    conn.close()
    
    return render_template('edit.html', post=post)


@app.route('/<int:id>/editpackage', methods=('GET', 'POST'))
def editpackage(id):
    post = get_post_package(id)
    if request.method == 'POST':
        packagename = request.form['packagename']
        description = request.form['description']
        price = request.form['price']
        person = request.form['person']
        food = request.form['food']
        

        if not packagename:
            flash('Package name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE packages SET packagename = ?, description = ?, price = ?, person = ?, food = ?'
                         ' WHERE id = ?',
                         (packagename, description,price,person,food,id))
            conn.commit()
            conn.close()
            return redirect(url_for('viewpackage'))
        
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM packages').fetchall()
    conn.close()
    
    return render_template('editpackage.html', post=post)


def validate(username, password):
    con = sqlite3.connect('database.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[3]
                    dbPass = row[4]
                    if dbUser==username and dbPass==password:
                        completion = True
    return completion


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('adminlogin.html', error=error)


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/chooseus')
def chooseus():
    
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM packages').fetchall()
    conn.close()
    return render_template('chooseus.html', posts=posts)

@app.route('/packages')
def packages():
    
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM packages').fetchall()
    conn.close()
    return render_template('packages.html', posts=posts)

