from flask_sqlalchemy import SQLAlchemy
from flask import abort
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from flask_migrate import Migrate
import os

load_dotenv()

db_name = os.getenv('PSQL_DATABASE')
password = os.getenv('PSQL_PASSWORD')
host = os.getenv('PSQL_HOST')
user = os.getenv('PSQL_USER')
port = 5432
db_path = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

db = SQLAlchemy()


def setup_psql(app, database_path=db_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Usuario(db.Model):
    __tablename__ = 'usuario'
    dni = db.Column(db.Integer, primary_key=True, nullable=True)
    nombres = db.Column(db.String(200), nullable=False)
    apellidos = db.Column(db.String(200), nullable=False)
    correo = db.Column(db.String(200), nullable=False, unique=True)
    celular = db.Column(db.String(200), nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    estudiantes = db.relationship(
        'Estudiante', backref='estudiante', lazy=True, cascade="all, delete-orphan")
    repartidores = db.relationship(
        'Repartidor', backref='repartidor', lazy=True, cascade='all, delete-orphan')

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.dni
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Usuario('{self.dni}', \nNombres:'{self.nombres}', \nApellidos:'{self.apellidos}', \nCorreo:'{self.correo}', \nCelular:'{self.celular}', \Sexo:'{self.sexo}', \nPassword:'{self.password}')"

    def format(self):
        return {
            "dni": self.dni,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "correo": self.correo,
            "celular": self.celular,
            "sexo": self.sexo,
            "password": self.password
        }


class Repartidor(db.Model):
    __tablename__ = 'repartidor'
    dni = db.Column(db.Integer, db.ForeignKey(
        "usuario.dni"), primary_key=True, nullable=False)
    vehiculoModelo = db.Column(db.String(200), nullable=False)
    placa = db.Column(db.String(20), nullable=False)
    comprobantes_virtuales = db.relationship(
        'ComprobanteVirtual', backref='comprobante_virtual', lazy=True, cascade='all, delete-orphan')

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.dni
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Repartidor('{self.dni}', '{self.vehiculoModelo}', '{self.placa}')"

    def format(self):
        return {
            "usuario_id": self.dni,
            "vehiculoModelo": self.vehiculoModelo,
            "placa": self.placa
        }


class Estudiante(db.Model):
    __tablename__ = "estudiante"
    dni = db.Column(db.Integer, db.ForeignKey(
        "usuario.dni"), primary_key=True, nullable=False)
    IE = db.Column(db.String(200), nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.dni
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Alumno('{self.dni}', '{self.IE}')"

    def format(self):
        return {
            "user_id": self.dni,
            "Institucion Educativa": self.IE
        }


class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Float, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(30), nullable=False)
    fecha_vencimiento = db.Column(db.DateTime, primary_key=True)
    vencido = db.Column(db.Boolean, nullable=False)
    almacenes = db.relationship(
        'Almacen', backref='almacen', lazy=True, cascade='all, delete-orphan')
    compras = db.relationship(
        'Compra', backref='compra', lazy=True, cascade='all, delete-orphan')
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()
    
    def update(self):
        try:
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"<Producto id={self.id}>"
    
    def format(self):
        return {
            "id": self.id,
            "precio" : self.precio,
            "nombre" : self.nombre,
            "descripcion" : self.descripcion,
            "categoria" : self.categoria,
            "fecha_vencimiento" : self.fecha_vencimiento,
            "vencido" : self.vencido
        }
    

class PuntosRecojo(db.Model):
    __tablename__ = 'puntos_recojo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    abierto = db.Column(db.Boolean, nullable=False, default=True)
    almacenes = db.relationship(
        'Almacen', backref='almacen', lazy=True, cascade='all, delete-orphan')
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def update(self):
        try:
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"<PuntosRecojo id={self.id}>"
    
    def format(self):
        return {
            "id": self.id,
            "nombre" : self.nombre,
            "direccion" : self.direccion,
            "abierto" : self.abierto,
        }
    

class Comprobante(db.Model):
    __tablename__ = 'comprobante'
    codigo = db.Column(db.Integer, primary_key=True, nullable=False)
    dni = db.Column(db.Integer, db.ForeignKey(
        "estudiante.dni"), primary_key=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    fisicos = db.relationship(
        'ComprobanteFisico', backref='comprobante_fisico', lazy=True, cascade='all, delete-orphan')
    virtuales = db.relationship(
        'ComprobanteVirtual', backref='comprobante_virtual', lazy=True, cascade='all, delete-orphan')
    compras = db.relationship(
        'Compra', backref='compra', lazy=True, cascade='all, delete-orphan')

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.codigo
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Comprobante('{self.codigo}', \Dni:'{self.dni}', \Monto:'{self.monto}', \Fecha:'{self.fecha}')"

    def format(self):
        return {
            "codigo": self.codigo,
            "dni": self.dni,
            "monto": self.monto,
            "fecha": self.fecha
        }
    

class ComprobanteFisico(db.Model):
    __tablename__ = 'comprobante_fisico'
    codigo = db.Column(db.Integer, db.ForeignKey(
        "comprobante.codigo"), primary_key=True, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    recogido = db.Column(db.Boolean, nullable=False, default=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.codigo
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"ComprobanteFisico('{self.codigo}', '{self.direccion}', '{self.recogido}')"

    def format(self):
        return {
            "codigo": self.codigo,
            "direccion": self.direccion,
            "recogido": self.recogido
        }


class ComprobanteVirtual(db.Model):
    __tablename__ = "comprobante_virtual"
    codigo = db.Column(db.Integer, db.ForeignKey(
        "comprobante.codigo"), primary_key=True, nullable=False)
    repartidor_dni = db.Column(db.Integer, db.ForeignKey(
        "repartidor.dni"), primary_key=False, nullable=False)
    entregado = db.Column(db.Boolean, nullable=False, default=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.codigo
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"ComprobanteVirtual('{self.codigo}', '{self.repartidor_dni}','{self.entregado}')"

    def format(self):
        return {
            "codigo": self.codigo,
            "repartidor_dni": self.repartidor_dni,
            "entregado": self.entregado
        }

class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer, db.ForeignKey(
        "comprobante.codigo"), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey(
        "producto.id"), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Compra('{self.id}', \Producto ID:'{self.producto_id}', \Cantidad:'{self.cantidad}')"

    def format(self):
        return {
            "id": self.id,
            "producto ID": self.producto_id,
            "cantidad": self.cantidad
        }
    
class Almacen(db.Model):
    __tablename__ = 'almacen'
    pr_id = db.Column(db.Integer, db.ForeignKey(
        "puntos_recojo.id"), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey(
        "producto.id"), primary_key=True)
    fecha_vencimiento = db.Column(db.DateTime, db.ForeignKey(
        "producto.fecha_vencimiento"), primary_key=True)
    stock = db.Column(db.Integer, nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.pr_id, self.producto_id
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Almacen('{self.pr_id}', \Producto ID:'{self.producto_id}', \Fecha Vencimiento:'{self.fecha_vencimiento}', \Stock:'{self.stock}')"

    def format(self):
        return {
            "punto de recojo ID": self.pr_id,
            "producto ID": self.producto_id,
            "stock": self.stock
        }