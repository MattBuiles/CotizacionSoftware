import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

# Ruta Absoluta para evitar problemas de acceso
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'cotizaciones.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cotizacion(db.Model):
    #Atributos base
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=func.current_date())
    ciudad = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    proyecto = db.Column(db.String(100), nullable=False)
    plazo = db.Column(db.String(100), nullable=False)
    entrega = db.Column(db.String(100), nullable=False)
    anticipo = db.Column(db.Integer, nullable=False)
    p_acta = db.Column(db.Integer, nullable=False)
    f_acta= db.Column(db.Integer, nullable=False)
    consecutivo = db.Column(db.Integer, nullable=False)
    # Relación auto-referencial para versiones
    version_padre_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'), nullable=True)
    versiones = db.relationship('Cotizacion', backref=db.backref('version_padre', remote_side=[id]), lazy=True)
    #Atributos definibles por el usuario
    productos = db.relationship('Producto', back_populates='cotizacion', order_by='Producto.id')
    servicio = db.Column(db.String(1000), nullable=False)
    def __repr__(self):
        return f'<Cotizacion {self.id} - Cliente: {self.cliente} - Empresa: {self.empresa}>'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    # Clave foránea para referenciar a Cotizacion
    cotizacion_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'))
    # Relación con Cotizacion
    cotizacion = db.relationship('Cotizacion', back_populates='productos')
    def __repr__(self):
        return f'<Producto {self.id} - Nombre: {self.nombre}>'

@app.route("/")
def index():
    return render_template("index.html",)


@app.route("/crear_cotizacion")
def create_quote():
    return render_template("crear_cotizacion.html")


@app.route('/ver_cotizacion', methods=['POST'])
def crear_cotizacion():
    ciudad = request.form['ciudad']
    empresa = request.form['empresa_cliente_nombre']
    cliente = request.form['cliente_nombre']
    celular = request.form['cliente_celular']
    email = request.form['cliente_correo']
    proyecto = request.form['nombre_proyecto']
    plazo = request.form['plazo_oferta']
    entrega = request.form['tiempo_entrega']
    anticipo = request.form['porcentaje_anticipo']
    p_acta = request.form['porcentaje_primera_acta']
    f_acta = request.form['porcentaje_acta_final']
    consecutivo = 1
    producto_seleccionado=None
    servicio_ingresado=None


    opcion = request.form.get('producto_servicio')
    if opcion == 'producto':
        # Captura el valor del select de productos
        producto_seleccionado = request.form.get('producto')
    
    elif opcion == 'servicio':
        # Captura el valor del campo de texto para servicios
        servicio_ingresado = request.form.get('servicio')

    #! Código de los productos a modificar
    """
    productos = []
    for i in range(1, 5):
        descripcion = request.form.get(f'productos[{i-1}][descripcion]')
        cantidad = request.form.get(f'productos[{i-1}][cantidad]')
        precio = request.form.get(f'productos[{i-1}][precio]')

        if descripcion and cantidad and precio:
            total_producto = float(cantidad) * float(precio)
            productos.append({
                'descripcion': descripcion,
                'cantidad': cantidad,
                'precio_unitario': precio,
                'total': total_producto
            })
    """

    cotizacion = Cotizacion(ciudad=ciudad, empresa=empresa, cliente=cliente, celular=celular, email=email, proyecto=proyecto, plazo=plazo, entrega=entrega, anticipo=anticipo, p_acta=p_acta, f_acta=f_acta, consecutivo=consecutivo, servicio=servicio_ingresado)
    db.session.add(cotizacion)
    db.session.commit()

    """
    for producto in productos:
        producto_db = Producto(
            cotizacion_id=cotizacion.id,
            descripcion=producto['descripcion'],
            cantidad=producto['cantidad'],
            precio_unitario=producto['precio_unitario'],
            total=producto['total']
        )
        db.session.add(producto_db)
    db.session.commit()
    """

    return render_template('cotizacion_final.html', cotizacion=cotizacion)

@app.route('/lista_cotizaciones')
def listar_cotizaciones():
    cotizaciones = Cotizacion.query.all()
    return render_template('lista_cotizaciones.html', cotizaciones=cotizaciones)


@app.route('/cotizacion/<int:id>')
def ver_cotizacion(id):
    cotizacion = Cotizacion.query.get_or_404(id)
    productos = Producto.query.filter_by(cotizacion_id=id).all()
    return render_template('ver_cotizacion.html', cotizacion=cotizacion, productos=productos)

if __name__ == '__main__':
    # Creación de tablas con logging adicional para debug
    with app.app_context():
        db.create_all()

    app.run(debug=True)
