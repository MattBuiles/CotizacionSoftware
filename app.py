import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
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
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=lambda: datetime.now(pytz.timezone('America/Bogota')).date())
    ciudad = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    proyecto = db.Column(db.String(100), nullable=False)
    plazo = db.Column(db.String(100), nullable=False)
    entrega = db.Column(db.String(100), nullable=False)
    anticipo = db.Column(db.Integer, nullable=False)
    p_acta = db.Column(db.Integer, nullable=False)
    f_acta= db.Column(db.Integer, nullable=False)
    consecutivo = db.Column(db.Integer, nullable=False)
    version_padre_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'), nullable=True)
    versiones = db.relationship('Cotizacion', backref=db.backref('version_padre', remote_side=[id]), lazy=True)
    productos_detalle = db.relationship('CotizacionProducto', backref='cotizacion', lazy=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', backref=db.backref('cotizaciones', lazy=True))
    servicio = db.Column(db.String(1000), nullable=False, default="v")

    def __repr__(self):
        return f'<Cotizacion {self.id} - Cliente: {self.cliente.nombre} - Empresa: {self.empresa}>'
    
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Cliente {self.nombre}>'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)

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
    return render_template("index.html")

@app.route("/crear_cotizacion")
def create_quote():
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return render_template("crear_cotizacion.html", clientes=clientes, productos=productos)

@app.route('/ver_cotizacion', methods=['POST'])
def crear_cotizacion():
    cliente_id = request.form.get('cliente_existente')
    if cliente_id:
        cliente = Cliente.query.get(cliente_id)
    else:
        nombre_cliente = request.form['cliente_nombre']
        email_cliente = request.form['cliente_correo']
        telefono_cliente = request.form.get('cliente_celular')
        cliente = Cliente(nombre=nombre_cliente, email=email_cliente, celular=telefono_cliente)
        db.session.add(cliente)
        db.session.commit()

    ciudad = request.form['ciudad']
    empresa = request.form['empresa_cliente_nombre']
    proyecto = request.form['nombre_proyecto']
    plazo = request.form['plazo_oferta']
    entrega = request.form['tiempo_entrega']
    anticipo = request.form['porcentaje_anticipo']
    p_acta = request.form['porcentaje_primera_acta']
    f_acta = request.form['porcentaje_acta_final']

    # Obtener la siguiente versión para este cliente
    version = get_next_version(cliente.id)

    opcion = request.form.get('producto_servicio')
    if opcion == 'producto':
        cotizacion = Cotizacion(
            ciudad=ciudad,
            empresa=empresa,
            proyecto=proyecto,
            plazo=plazo,
            entrega=entrega,
            anticipo=anticipo,
            p_acta=p_acta,
            f_acta=f_acta,
            consecutivo=version,
            cliente=cliente,
            servicio="v",
            version_padre_id=None
        )
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
                detalle = CotizacionProducto(
                    cotizacion_id=cotizacion.id,
                    producto_id=producto_id,
                    cantidad=int(cantidad),
                    tamano=tamano
                )
                db.session.add(detalle)
        db.session.commit()
    
    elif opcion == 'servicio':
        servicio_ingresado = request.form.get('servicio')
        cotizacion = Cotizacion(
            ciudad=ciudad,
            empresa=empresa,
            proyecto=proyecto,
            plazo=plazo,
            entrega=entrega,
            anticipo=anticipo,
            p_acta=p_acta,
            f_acta=f_acta,
            consecutivo=version,
            cliente=cliente,
            servicio=servicio_ingresado,
            version_padre_id=None
        )
        db.session.add(cotizacion)
        db.session.commit()

    return render_template('cotizacion_final.html', cotizacion=cotizacion)

@app.route('/lista_cotizaciones')
def listar_cotizaciones():
    cotizaciones = Cotizacion.query.all()
    return render_template('lista_cotizaciones.html', cotizaciones=cotizaciones)

@app.route('/cotizacion/<int:id>')
def ver_cotizacion(id):
    cotizacion = Cotizacion.query.get_or_404(id)
    productos = CotizacionProducto.query.filter_by(cotizacion_id=id).all()
    return render_template('ver_cotizacion.html', cotizacion=cotizacion, productos=productos)

@app.route('/cotizacion_final')
def listar_cotizacion():
    cotizacion = Cotizacion.query.offset(3).first()
    return render_template('cotizacion_final.html', cotizacion=cotizacion)

@app.route('/editar_cotizacion/<int:id>')
def editar_cotizacion(id):
    cotizacion_original = Cotizacion.query.get_or_404(id)
    
    # Crear una nueva versión de la cotización
    version = get_next_version(cotizacion_original.cliente_id)
    nueva_cotizacion = Cotizacion(
        fecha=cotizacion_original.fecha,
        ciudad=cotizacion_original.ciudad,
        empresa=cotizacion_original.empresa,
        proyecto=cotizacion_original.proyecto,
        plazo=cotizacion_original.plazo,
        entrega=cotizacion_original.entrega,
        anticipo=cotizacion_original.anticipo,
        p_acta=cotizacion_original.p_acta,
        f_acta=cotizacion_original.f_acta,
        consecutivo=version,
        cliente=cotizacion_original.cliente,
        servicio=cotizacion_original.servicio,
        version_padre_id=cotizacion_original.id
    )
    
    db.session.add(nueva_cotizacion)
    db.session.commit()

    # Copiar los productos asociados a la cotización original
    for detalle in cotizacion_original.productos_detalle:
        nuevo_detalle = CotizacionProducto(
            cotizacion_id=nueva_cotizacion.id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            tamano=detalle.tamano
        )
        db.session.add(nuevo_detalle)
    
    db.session.commit()

    # Redirigir a la nueva cotización para su edición
    return render_template('crear_cotizacion.html', clientes=Cliente.query.all(), productos=Producto.query.all())

def get_next_version(cliente_id):
    last_version = db.session.query(db.func.max(Cotizacion.consecutivo)).filter_by(cliente_id=cliente_id).scalar()
    return (last_version or 0) + 1

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
