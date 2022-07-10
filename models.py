from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

database_name='park'
database_path='postgresql://{}@{}/{}'.format('postgres:5051111', 'localhost:5432', database_name)
db=SQLAlchemy()

def setup_db(app, databse_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI']=database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    db.create_all()

class Carro(db.Model):
    __tablename__='carros'
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Integer(), nullable=False)
    placa=db.Column(db.String(6), nullable=False)
    id_espacio=db.Column(db.Integer, db.ForeignKey('espacios.id'))    

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'date':self.date,
            'placa':self.placa,
            'id_espacio':self.id_espacio
        }

    def __repr__(self):
        return f'Carro: id={self.id}, date={self.date}, placa={self.placa}, id_espacio={self.id_espacio}'


class Espacio(db.Model):
    __tablename__='espacios'
    id=db.Column(db.Integer,primary_key=True)
    libre=db.Column(db.Boolean, nullable=False, default=True)
    carros = db.relationship('Carro', backref='espacio')

    def update(self):
        try:
            db.session.commit()
        except:
            db.sesion.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'libre': self.libre
        }

    def _repr_(self):
        return f'Espacio: id={self.id}, libre={self.libre}'

class Registro(db.Model):
    __tablename__ = 'registro'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(),unique= True,nullable = False)
    contra = db.Column(db.String(),unique= True,nullable = False) 
    admin = db.Column(db.Boolean(), default=False)    
    
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
        except:
            db.sesion.rollback()
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
    def format(self):
        return {
            'id': self.id,
            'usuario': self.usuario,
            'contra': self.contra,
            'admin':self.admin
        }

    def _repr_(self):
        return f'Registro: id={self.id}, usuario={self.usuario}, contra={self.contra}, admin={self.admin}'

class Pago(db.Model):
    __tablename__='pagos'
    id=db.Column(db.Integer, primary_key=True)
    placa=db.Column(db.String(7), nullable=False)
    monto=db.Column(db.Integer(), nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
            
    def format(self):
        return jsonify({
            'id':self.id,
            'placa':self.placa,
            'monto':self.monto
        })
        
    def _repr_(self):
        return f'Pago: id={self.id}, placa={self.placa}, monto={self.monto}'