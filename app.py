import sqlite3
from flask import (Flask, render_template, request, url_for, redirect, flash, get_flashed_messages, g)

app = Flask(__name__)

#configuraciones
app.secret_key = 'my_secret_key'
DATABASE = "Database"


@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BOOKS")
        
        #actualizar despues
        book_list = cursor.fetchall()

    return render_template('index.html',book_list=book_list)

#Agregar libro
@app.route('/add',methods=['POST'])
def add_book():
    if request.method == 'POST':
        book = request.form['book_name'] # 'book_name' es el name en el formulario
        author = request.form['author']
        year = request.form['year']

        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO BOOKS (name,author,year) VALUES(?,?,?)",(book,author,year))
            connection.commit()

        #Bug: en caso de error se generan dos inserciones , solucionar con patron de diseño
        flash('Libro agregado satisfactoriamente')
        return redirect(url_for('index'))

#Editar libro
@app.route('/edit')
def edit_book():
    return "Edit Book"

#Eliminar libro
@app.route('/delete/<string:id>')
def delete_book(id):
    with sqlite3.connect("Database") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM BOOKS WHERE id = ?",(id,))
        connection.commit()
    flash('Libro eliminado satisfactoriamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 