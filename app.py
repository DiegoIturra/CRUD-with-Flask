import sqlite3
from flask import (Flask, render_template, request, url_for, redirect, flash, get_flashed_messages, g)

app = Flask(__name__)

#configuraciones
app.secret_key = 'my_secret_key'
DATABASE = "Database" #direccion de la base de datos , en misma carpeta para simplicidad


def get_db():
    """ Funcion que retorna una conexion a la base de datos , para evitar abrir y cerrar la conexion en cada peticion realizada por el usuario,
    mejorando de esta forma el rendimiento de la aplicación """
    db = getattr(g,'_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """ Funcion es llamada cuando el contexto de la aplicacion es finalizado, cerrando asi la conexion a la base de datos"""
    db = getattr(g,'_database',None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM BOOKS")
    book_list = cursor.fetchall()
    return render_template('index.html',book_list=book_list)

#Agregar libro
@app.route('/add',methods=['POST'])
def add_book():
    if request.method == 'POST':
        book = request.form['book_name'] # 'book_name' es el name en el formulario
        author = request.form['author']
        year = request.form['year']

        cursor = get_db().cursor()
        cursor.execute("INSERT INTO BOOKS (name,author,year) VALUES(?,?,?)",(book,author,year))
        get_db().commit()

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
    cursor = get_db().cursor()
    cursor.execute("DELETE FROM BOOKS WHERE id = ?",(id,))
    get_db().commit()
    flash('Libro eliminado satisfactoriamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 