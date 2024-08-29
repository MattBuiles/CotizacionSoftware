from app import db, Producto, Cliente, Cotizacion, app, CotizacionProducto

def agregar_productos_default():
    productos_default = [
        {'nombre': 'ASFALTEX', 'precio': 50000},
        {'nombre': 'FRAGUA RAPIDO', 'precio': 75000},
        {'nombre': 'HIDROSELLO', 'precio': 30000},
        {'nombre': 'POLIFLEX', 'precio': 100000},
    ]

    for prod in productos_default:
        producto = Producto(nombre=prod['nombre'], precio=prod['precio'])
        db.session.add(producto)

    db.session.commit()
    print("Productos default agregados a la base de datos.")

def agregar_clientes_default():
    clientes_default = [
        {'nombre': 'Cliente 1', 'celular': '1234567890', 'email': 'cliente1@example.com'},
        {'nombre': 'Cliente 2', 'celular': '9876543210', 'email': 'cliente2@example.com'},
        {'nombre': 'Cliente 3', 'celular': '5555555555', 'email': 'cliente3@example.com'},
        {'nombre': 'Juanito Alimana', 'celular': '6666666666', 'email': "juanito@alimana.com"}
    ]

    for cliente in clientes_default:
        cliente = Cliente(nombre=cliente['nombre'], celular=cliente['celular'], email=cliente['email'])
        db.session.add(cliente)
    db.session.commit()
    print("Clientes default agregados a la base de datos.")

def agregar_cotizaciones_default():
    cotizaciones_default = [
        {'ciudad': 'Bogotá', 'empresa': 'Empresa 1', 'proyecto': 'Proyecto 1', 'plazo': '30 (TREINTA)', 'entrega': '15 (QUINCE)', 'anticipo': 0.3, 'p_acta': 0.3, 'f_acta': 0.4, 'consecutivo': 1, 'cliente': 1},
        {'ciudad': 'Medellín', 'empresa': 'Empresa 2', 'proyecto': 'Proyecto 2', 'plazo': '45 (CUARENTA Y CINCO)', 'entrega': '20 (VEINTE)', 'anticipo': 0.3, 'p_acta': 0.3, 'f_acta': 0.4, 'consecutivo': 1, 'cliente': 2},
        {'ciudad': 'Cali', 'empresa': 'Empresa 3', 'proyecto': 'Proyecto 3', 'plazo': '60 (SESENTA)', 'entrega': '30 (TREINTA)', 'anticipo': 0.3, 'p_acta': 0.3, 'f_acta': 0.4, 'consecutivo': 1, 'cliente': 3},
    ]

    for cotizacion in cotizaciones_default:
        cliente = Cliente.query.get(cotizacion['cliente'])
        cotizacion = Cotizacion(ciudad=cotizacion['ciudad'], empresa=cotizacion['empresa'], proyecto=cotizacion['proyecto'], plazo=cotizacion['plazo'], entrega=cotizacion['entrega'], anticipo=cotizacion['anticipo'], p_acta=cotizacion['p_acta'], f_acta=cotizacion['f_acta'], consecutivo=cotizacion['consecutivo'], cliente=cliente)
        db.session.add(cotizacion)

        productos_seleccionados = [
        {"producto_id": 1, "cantidad": 10, "tamano": 20},
        {"producto_id": 2, "cantidad": 5, "tamano": 200},
        ]
        # Creación de las relaciones CotizacionProducto
        for item in productos_seleccionados:
            producto = Producto.query.get(item["producto_id"])
            cotizacion_producto = CotizacionProducto(
                cotizacion_id=cotizacion.id,
                producto_id=producto.id,
                cantidad=item["cantidad"],
                tamano=item["tamano"]
            )
            db.session.add(cotizacion_producto)

        # Commit final para guardar todo en la base de datos
        db.session.commit()
    db.session.commit()
    


    cotizaciones_default = [
        {'ciudad': 'Bogotá', 'empresa': 'Empresa 1', 'proyecto': 'Proyecto 1', 'plazo': '30 (TREINTA)', 'entrega': '15 (QUINCE)', 'anticipo': 0.3, 'p_acta': 0.3, 'f_acta': 0.4, 'consecutivo': 1, 'cliente': 1, 'servicio': "El servicio de la cotización 1"},
    ]

    for cotizacion in cotizaciones_default:
        cliente = Cliente.query.get(cotizacion['cliente'])
        cotizacion = Cotizacion(ciudad=cotizacion['ciudad'], empresa=cotizacion['empresa'], proyecto=cotizacion['proyecto'], plazo=cotizacion['plazo'], entrega=cotizacion['entrega'], anticipo=cotizacion['anticipo'], p_acta=cotizacion['p_acta'], f_acta=cotizacion['f_acta'], consecutivo=cotizacion['consecutivo'], cliente=cliente, servicio=cotizacion['servicio'])
        db.session.add(cotizacion)
    db.session.commit()
    print("Cotizaciones default agregadas a la base de datos.")


if __name__ == '__main__':
    with app.app_context():  # Crea una instancia de la aplicación Flask
        agregar_productos_default()
        agregar_clientes_default()
        agregar_cotizaciones_default()
