# Sistema de Gestión de Cotizaciones

Este es un sistema web desarrollado en Flask para la gestión de cotizaciones, permitiendo la creación, modificación y visualización de cotizaciones para proyectos, productos y servicios. El sistema también permite gestionar la información de los clientes y documentos asociados a cada cotización.

## Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Despliegue](#despliegue)
- [Enlace al Proyecto](#enlace-al-proyecto)

## Características

- **Gestión de Cotizaciones**: Crea, modifica y elimina cotizaciones.
- **Gestión de Clientes**: Registra clientes y asocia cotizaciones con ellos.
- **Gestión de Productos y Servicios**: Añade productos con cantidad y tamaño, o servicios a las cotizaciones.
- **Versionado de Cotizaciones**: Permite la modificación y versionado de cotizaciones sin perder el historial.
- **Interfaz Amigable**: Una interfaz web simple e intuitiva para facilitar la gestión de cotizaciones.

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto localmente:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/MattBuiles/CotizacionSoftware.git
   ```
2. Navega al directorio del proyecto:
  ```bash
  cd nombre-del-repositorio
  ```
3. Crea un entorno virtual:
  ```bash
  python -m venv venv
  ```
4. Activa el entorno virtual

5. Instala las dependencias:
  ```bash
  pip install -r requirements.txt
  ```
6. Ejecuta la aplicación:

  ```bash
  python app.py
  ```
  Accede a la aplicación en tu navegador web en http://127.0.0.1:5000.

## Uso
Para crear una cotización, navega a la página de creación de cotizaciones, selecciona los productos o servicios, y completa los detalles del cliente. Una vez completada, la cotización puede ser modificada o eliminada según sea necesario.

## Tecnologías
El sistema ha sido desarrollado utilizando las siguientes tecnologías:

Backend: Python con Flask
Frontend: HTML, CSS
Base de Datos: SQLite
ORM: SQLAlchemy

## Despliegue
El proyecto ha sido desplegado y está disponible en el siguiente enlace:
[Acceder al sistema de cotizaciones](https://cotizacionsoftware.onrender.com)

## Enlace al Proyecto
Página desplegada: https://cotizacionsoftware.onrender.com
Repositorio GitHub: https://github.com/MattBuiles/CotizacionSoftware
