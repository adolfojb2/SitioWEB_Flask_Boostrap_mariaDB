from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from decouple import config

app = Flask(__name__)

web_brushDB = MySQL()
app.config['MYSQL_DATABASE_HOST'] = config('HOST_DB')
app.config['MYSQL_DATABASE_USER'] = config('USER_DB')
app.config['MYSQL_DATABASE_PASSWORD'] = config('PASSWORD_DB')
app.config['MYSQL_DATABASE_DB'] = config('DATABASE')
web_brushDB.init_app(app)

@app.route('/login',methods=['POST','GET'])
def login():
    msg = ''
    if request.method=='POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        #Validación de los datos en la BD
        cur = web_brushDB.get_db().cursor()
        cur.execute('SELECT*FROM usuarios WHERE correo=%s AND contrasena=%s',(correo,contrasena))
        account = cur.fetchone()
        cur.close()
        if account:
            print('Sesion iniciada')
            msg = 'Sesión iniciada!'
        else:
            print('Usuario o contraseña incorrectos!')
            msg = 'Usuario o contraseña incorrectos!'    
        return render_template('login.html', msg = msg)
    else:
        return render_template('login.html')

@app.route('/registro',methods=['POST','GET'])
def registro():
    if request.method=='POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        tel = int(request.form['tel'])
        cur = web_brushDB.get_db().cursor()
        cur.execute('INSERT INTO usuarios(nombre,correo,contrasena,tel)VALUES(%s,%s,%s,%s);',(nombre,correo,contrasena,tel))
        web_brushDB.get_db().commit() #se confirman los datos ingresados
        return render_template('registro.html')
    else:    
        return render_template('registro.html')
             

@app.route('/')
def index():
    cur = web_brushDB.get_db().cursor()
    cur.execute('SELECT * FROM usuarios') #ejecuta: seleccionar todas las columnas de la tabla numeros
    usuarios = cur.fetchall() #asigna una lista de tuplas

    return render_template('index.html', usuarios=usuarios)


@app.route('/crud_productos',methods=['POST','GET'])
def crud_productos():
    if request.method=='POST':
        producto = request.form['producto']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        stock = request.form['stock']
        precio = request.form['precio']
        # Ingresar los datos a la DB
        cur = web_brushDB.get_db().cursor()
        cur.execute('INSERT INTO productos(producto,descripcion,categoria,stock,precio)VALUES(%s,%s,%s,%s,%s);',(producto,descripcion,categoria,stock,precio))
        web_brushDB.get_db().commit() #se confirman los datos ingresados

    # Se optienen los datos de la DB
    cur = web_brushDB.get_db().cursor()
    cur.execute('SELECT * FROM productos') 
    productos = cur.fetchall()
    return render_template('crud_productos.html',productos=productos)

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/add_products')
def add_products():
    return render_template('add_products.html')    

@app.route('/edit_products')
def edit_products():
    return render_template('edit_products.html')       

if __name__ == '__main__':
    app.run(debug=True)

