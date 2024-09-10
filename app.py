"""
This file contains the implementation of a Flask web application for creating and managing quotations.
Classes:
- Cotizacion: Represents a quotation with various attributes such as date, city, company, project, etc.
- Cliente: Represents a client with attributes like name, phone number, and email.
- Producto: Represents a product with attributes like name and price.
- CotizacionProducto: Represents the relationship between a quotation and a product, including quantity and size.
Routes:
- index: Renders the index.html template.
- create_quote: Renders the crear_cotizacion.html template for creating a new quotation.
- crear_cotizacion: Handles the form submission for creating a new quotation.
- listar_cotizaciones: Renders the lista_cotizaciones.html template for listing all quotations.
- ver_cotizacion: Renders the ver_cotizacion.html template for viewing a specific quotation.
- listar_cotizacion: Renders the cotizacion_final.html template for testing the generation of a quotation.
Functions:
- index: Renders the index.html template.
- create_quote: Renders the crear_cotizacion.html template for creating a new quotation.
- crear_cotizacion: Handles the form submission for creating a new quotation.
- listar_cotizaciones: Renders the lista_cotizaciones.html template for listing all quotations.
- ver_cotizacion: Renders the ver_cotizacion.html template for viewing a specific quotation.
- listar_cotizacion: Renders the cotizacion_final.html template for testing the generation of a quotation.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
import pytz
import cloudinary.uploader
from config import *

app = Flask(__name__)
app.secret_key = 'BWvTvS8DxBkMp9Dp8p-jxYbsgWE'

# Ruta Absoluta para evitar problemas de acceso
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'cotizaciones.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

clientez = None
infoz = None


class Cotizacion(db.Model):
    # Atributos base
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=lambda: datetime.now(pytz.timezone('America/Bogota')).date())
    ciudad = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    proyecto = db.Column(db.String(100), nullable=False)
    plazo = db.Column(db.String(100), nullable=False)
    entrega = db.Column(db.String(100), nullable=False)
    anticipo = db.Column(db.Integer, nullable=False)
    p_acta = db.Column(db.Integer, nullable=False)
    f_acta = db.Column(db.Integer, nullable=False)
    consecutivo = db.Column(db.Integer, nullable=False)
    # Relación auto-referencial para versiones
    version_padre_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'), nullable=True)
    versiones = db.relationship('Cotizacion', backref=db.backref('version_padre', remote_side=[id]), lazy=True)
    # Atributos definibles por el usuario
    # Relación con CotizacionProducto
    productos_detalle = db.relationship('CotizacionProducto', backref='cotizacion', lazy=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', backref=db.backref('cotizaciones', lazy=True))
    servicio = db.Column(db.String(1000), nullable=False, default="v")

    def __repr__(self):
        return f'<Cotizacion {self.id} - Cliente: {self.cliente} - Empresa: {self.empresa}>'


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    # Relación con Cotizacion
    """
    cotizacion_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'))
    cotizaciones = db.relationship('Cotizacion', back_populates='clienten', order_by='Cotizacion.id')
    """

    def __repr__(self):
        return f'<Cliente {self.nombre}>'


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    # cotizacion_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'), nullable=False)
    # cotizacion = db.relationship('Cotizacion', backref=db.backref('productos', lazy=True))

    def __repr__(self):
        return f'<Producto {self.nombre}>'


class CotizacionProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cotizacion_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    tamano = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Producto', backref=db.backref('cotizacion_producto', lazy=True))

    def __repr__(self):
        return f'<CotizacionProducto: Producto {self.producto.nombre}, Cantidad: {self.cantidad}, Tamaño: {self.tamano}>'

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_subida = db.Column(db.Date, default=lambda: datetime.now(pytz.timezone('America/Bogota')).date())
    proyecto = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Document: Nombre {self.nombre}, URL: {self.url}, Proyecto: {self.proyecto}>'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/lista_proyectos')
def lista_proyectos():
    cotizaciones = Cotizacion.query.all()
    return render_template('lista_proyectos.html', cotizaciones=cotizaciones)

@app.route('/documentos/<proyecto>')
def listar_documentos(proyecto):
    cotizaciones = Cotizacion.query.filter_by(proyecto=proyecto).all()

    documentos = [
        {"nombre": "Documento1.pdf", "url": "https://drive.google.com/..."},
        {"nombre": "Documento2.pdf", "url": "https://drive.google.com/..."}
    ]

    return render_template('documentos.html', documentos=documentos, proyecto=proyecto)

@app.route('/documentos', methods=["GET",'POST'])
def mostrar_documentos():
    # Recupera todos los documentos de la base de datos
    documentos = Document.query.all()
    return render_template('documentos_proyecto.html', documentos=documentos)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica si el archivo ha sido subido
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo')
        return redirect(url_for('subir_archivo'))
    
    file = request.files['file']

    # Verifica si el archivo tiene un nombre
    if file.filename == '':
        flash('Archivo no válido')
        return redirect(url_for('subir_archivo'))

    if file:
        try:
            # Sube el archivo a Cloudinary
            result = cloudinary.uploader.upload(file, secure=True)
            
            # Guarda la URL en la base de datos
            nuevo_documento = Document(url=result['secure_url'],nombre=file.filename,  proyecto="Proyecto 1")
            db.session.add(nuevo_documento)
            db.session.commit()
            
            flash('Archivo subido exitosamente')
            return redirect(url_for('mostrar_documentos'))
        except Exception as e:
            flash(f'Error al subir el archivo: {str(e)}')
            return redirect(request.url)

@app.route('/subir_archivo', methods=["GET",'POST'])
def subir_archivo():
    return render_template('subir_archivo.html')

@app.route("/soporte")
def soporte():
    return render_template("soporte.html")

@app.route("/usuario_cotizacion", methods=["GET", "POST"])
def userManager():
    clientes = Cliente.query.all()
    return render_template("usuario_cotizacion.html", clientes=clientes)

@app.route("/producto_servicio", methods=["GET", "POST"])
def product_service():
    # Datos de cotización
    ciudad = request.form['ciudad']
    empresa = request.form['empresa_cliente_nombre']
    proyecto = request.form['nombre_proyecto']
    plazo = request.form['plazo_oferta']
    entrega = request.form['tiempo_entrega']
    anticipo = request.form['porcentaje_anticipo']
    p_acta = request.form['porcentaje_primera_acta']
    f_acta = request.form['porcentaje_acta_final']
    consecutivo = 1

    info=[ciudad,empresa, proyecto,plazo, entrega, anticipo, p_acta, f_acta, consecutivo]
    global infoz
    infoz=info
    productos = Producto.query.all()
    return render_template("producto_servicio.html", productos=productos)

@app.route("/crear_cotizacion", methods=['POST'])
def cotizacion():
    tipo_usuario = request.form.get('tipo_usuario')
    cliente = None
    if tipo_usuario == 'registrado':
        cliente_id = request.form.get('cliente_existente')
        cliente = Cliente.query.get(cliente_id)
    elif tipo_usuario == 'nuevo':
        nombre_cliente = request.form.get('cliente_nombre')
        celular_cliente = request.form.get('cliente_celular')
        correo_cliente = request.form.get('cliente_correo')
        # Crear nuevo cliente
        cliente = Cliente(nombre=nombre_cliente, celular=celular_cliente, email=correo_cliente)
        db.session.add(cliente)
        db.session.commit()
    global clientez
    clientez = cliente
    return render_template("crear_cotizacion.html")


@app.route('/ver_cotizacion', methods=['POST'])
def crear_cotizacion():
    # Datos del producto o servicio
    opcion = request.form.get('producto_servicio')
    global infoz
    info = infoz
    global clientez
    cliente = clientez

    ciudad = info[0]
    empresa = info[1]
    proyecto = info[2]
    plazo = info[3]
    entrega = info[4]
    anticipo = info[5]
    p_acta = info[6]
    f_acta = info[7]
    consecutivo = info[8]

    if opcion == 'producto':
        # Captura el valor del select de productos
        cotizacion = Cotizacion(ciudad=ciudad, empresa=empresa, proyecto=proyecto, plazo=plazo, entrega=entrega,anticipo=anticipo, p_acta=p_acta, f_acta=f_acta, consecutivo=consecutivo, cliente=cliente)
        db.session.add(cotizacion)
        db.session.commit()

        # Obtener los productos seleccionados
        for producto in Producto.query.all():
            if request.form.get(f'cantidad{producto.id}'):
                cantidad = int(request.form.get(f'cantidad{producto.id}'))
                tamano = request.form.get(f'tamano{producto.id}')
                if tamano == 'CUNETE':
                    tamano = 4
                elif tamano == 'GALON':
                    tamano = 20
                elif tamano == 'TAMBOR':
                    tamano = 200
                detalle = CotizacionProducto(cotizacion_id=cotizacion.id, producto_id=producto.id, cantidad=int(cantidad), tamano=tamano)
                db.session.add(detalle)
        db.session.commit()

    elif opcion == 'servicio':
        # Captura el valor del campo de texto para servicios
        servicio_ingresado = request.form.get('servicio')
        cotizacion = Cotizacion(ciudad=ciudad, empresa=empresa, proyecto=proyecto, plazo=plazo, entrega=entrega, anticipo=anticipo,p_acta=p_acta, f_acta=f_acta, consecutivo=consecutivo, cliente=cliente, servicio=servicio_ingresado)
        db.session.add(cotizacion)
        db.session.commit()

    return render_template('cotizacion_final.html', cotizacion=cotizacion)


@app.route('/lista_cotizaciones')
def listar_cotizaciones():
    cotizaciones = Cotizacion.query.all()
    return render_template('lista_cotizaciones.html', cotizaciones=cotizaciones)

@app.route('/versiones_cotizacion/<int:id>')
def listar_versiones(id):
    cotizacion = Cotizacion.query.get_or_404(id)
    # Obtener todas las versiones de esta cotización, ordenadas por consecutivo descendente
    versiones = Cotizacion.query.filter_by(version_padre_id=cotizacion.id).order_by(Cotizacion.consecutivo.desc()).all()
    # Obtener la cotización actual y todas las versiones padres (incluyendo abuelo si existe)
    padres = []
    padre = cotizacion.version_padre
    while padre:
        padres.append(padre)
        padre = padre.version_padre
    padres.reverse()  # Para mostrar desde el más antiguo al más reciente

    return render_template('versiones_cotizacion.html', cotizacion=cotizacion, versiones=versiones, padres=padres)


@app.route('/cotizacion/<int:id>')
def ver_cotizacion(id):
    cotizacion = Cotizacion.query.get_or_404(id)
    return render_template('ver_cotizacion.html', cotizacion=cotizacion)

@app.route('/cotizacion_modificacion/<int:id>', methods=['POST'])
def modificar_cotizacion(id):
    cotizacion = Cotizacion.query.get_or_404(id)
    return render_template('modificar_cotizacion.html', cotizacion=cotizacion)


@app.route('/actualizar_cotizacion/<int:id>', methods=['POST'])
def actualizar_cotizacion(id):
    cotizacion = Cotizacion.query.get_or_404(id)
    
    # Crear nueva cotización como una versión
    nueva_cotizacion = Cotizacion(
        fecha=cotizacion.fecha,
        ciudad=request.form['ciudad'],
        empresa=request.form['empresa'],
        proyecto=cotizacion.proyecto,
        plazo=cotizacion.plazo,
        entrega=cotizacion.entrega,
        anticipo=cotizacion.anticipo,
        p_acta=cotizacion.p_acta,
        f_acta=cotizacion.f_acta,
        consecutivo=cotizacion.consecutivo + 1,
        cliente=cotizacion.cliente,
        servicio=cotizacion.servicio,
        version_padre_id=cotizacion.id
    )
    
    db.session.add(nueva_cotizacion)
    db.session.commit()
    
    # Redirigir a la vista de la nueva cotización
    return redirect(url_for('ver_cotizacion', id=nueva_cotizacion.id))


# Metodo para probar generación de cotización
"""
@app.route('/cotizacion_final', methods=['POST'])
def listar_cotizacion():
    # Obtener la cuarta cotización de la base de datos
    cotizacion = Cotizacion.query.offset(3).first()
    return render_template('cotizacion_final.html', cotizacion=cotizacion)
"""

if __name__ == '__main__':
    # Creación de tablas con logging adicional para debug
    with app.app_context():
        db.create_all()

    app.run(debug=True)