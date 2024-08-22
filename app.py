import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Ruta Absoluta para evitar problemas de acceso
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'cotizaciones.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cotizacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    impuesto = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cotizacion_id = db.Column(db.Integer, db.ForeignKey(
        'cotizacion.id'), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    cotizacion = db.relationship('Cotizacion', back_populates='productos')


Cotizacion.productos = db.relationship(
    'Producto', order_by=Producto.id, back_populates='cotizacion')


@app.route('/')
def index():
    return render_template('cotizacion.html')


@app.route('/crear_cotizacion', methods=['POST'])
def crear_cotizacion():
    cliente = request.form['cliente']

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

    subtotal = sum(p['total'] for p in productos)
    impuesto = subtotal * 0.15
    total = subtotal + impuesto

    cotizacion = Cotizacion(
        cliente=cliente, subtotal=subtotal, impuesto=impuesto, total=total)
    db.session.add(cotizacion)
    db.session.commit()

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

    return render_template('cotizacion_final.html', cliente=cliente, productos=productos, subtotal=subtotal, impuesto=impuesto, total=total)

@app.route('/cotizaciones')
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
        print("Creando tablas...")
        db.create_all()
        print("Tablas creadas. Base de datos inicializada.")

    app.run(debug=True)
