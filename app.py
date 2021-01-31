from flask import Flask,render_template,request,url_for,redirect,flash,get_flashed_messages
from books import book_list

app = Flask(__name__)

#configuraciones
app.secret_key = 'my_secret_key'

@app.route('/')
def index():
    return render_template('index.html',book_list=book_list)

#Agregar libro
@app.route('/add',methods=['POST'])
def add_book():
    if request.method == 'POST':
        fullname = request.form['fullname'] # 'fullname' es el name en el formulario
        book_list.append(fullname)
        flash('Libro agregado satisfactoriamente')
        return redirect(url_for('index',book_list=book_list))

#Editar libro
@app.route('/edit')
def edit_book():
    return "Edit Book"

#Eliminar libro
@app.route('/delete')
def delete_book():
    return "Delete Book"

if __name__ == '__main__':
    app.run(debug=True) 