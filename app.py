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
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
import pytz

app = Flask(__name__)

# Ruta Absoluta para evitar problemas de acceso
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'cotizaciones.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
    cotizacion_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'), nullable=False)
    cotizacion = db.relationship('Cotizacion', backref=db.backref('productos', lazy=True))

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


@app.route("/")
def index():
    return render_template("index.html",)


@app.route("/usuario_cotizacion")
def userManager():
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return render_template("usuario_cotizacion.html", clientes=clientes, productos=productos)


@app.route("/crear_cotizacion")
def cotiacion():
    return render_template("crear_cotizacion.html",)


@app.route("/producto_servicio")
def product_service():
    return render_template("producto_servicio.html",)


@app.route('/ver_cotizacion', methods=['POST'])
def crear_cotizacion():
    # Datos del cliente
    cliente_id = request.form.get('cliente_existente')
    if cliente_id:
        cliente = Cliente.query.get(cliente_id)
    else:
        nombre_cliente = request.form['cliente_nombre']
        email_cliente = request.form['cliente_celular']
        telefono_cliente = request.form.get('cliente_correo')
        cliente = Cliente(nombre=nombre_cliente, email=email_cliente, celular=telefono_cliente)
        db.session.add(cliente)
        db.session.commit()

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

    # Datos del producto o servicio
    opcion = request.form.get('producto_servicio')
    if opcion == 'producto':
        # Captura el valor del select de productos
        cotizacion = Cotizacion(ciudad=ciudad, empresa=empresa, proyecto=proyecto, plazo=plazo, entrega=entrega,anticipo=anticipo, p_acta=p_acta, f_acta=f_acta, consecutivo=consecutivo, cliente=cliente, productos=productos)
        db.session.add(cotizacion)
        db.session.commit()

        producto_ids = request.form.getlist('productos')

        for producto_id in producto_ids:
            cantidad = request.form.get(f'cantidad_{producto_id}')
            tamano = request.form.get(f'tamano_{producto_id}')
            if cantidad and tamano:
                if tamano == 'CUNETE':
                    tamano = 4
                elif tamano == 'GALON':
                    tamano = 20
                elif tamano == 'TAMBOR':
                    tamano = 200
                detalle = CotizacionProducto(cotizacion_id=cotizacion.id, producto_id=producto_id, cantidad=int(cantidad), tamano=tamano)
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

@app.route('/cotizacion/<int:id>')

@app.route('/cotizacion/<int:id>')
def ver_cotizacion(id):
    cotizacion = Cotizacion.query.get_or_404(id)
    return render_template('ver_cotizacion.html', cotizacion=cotizacion)

# Metodo para probar generación de cotización
@app.route('/cotizacion_final')
def listar_cotizacion():
    # Obtener la cuarta cotización de la base de datos
    cotizacion = Cotizacion.query.offset(3).first()
    return render_template('cotizacion_final.html', cotizacion=cotizacion)


if __name__ == '__main__':
    # Creación de tablas con logging adicional para debug
    with app.app_context():
        db.create_all()

    app.run(debug=True)
