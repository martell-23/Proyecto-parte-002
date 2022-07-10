from datetime import datetime
from flask import Flask, abort, jsonify, request, render_template
from flask_cors import CORS
import flask_sqlalchemy
from models import setup_db, Carro, Espacio, Registro, Pago

A=Espacio()
B=Espacio()
C=Espacio()
D=Espacio()
F=Espacio()
G=Espacio()
H=Espacio()
I=Espacio()
J=Espacio()
K=Espacio()

TODOS_PER_PAGE=5

def paginate(request, seleccion):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*TODOS_PER_PAGE
    end = start + TODOS_PER_PAGE

    todos = [todo.format() for todo in seleccion]
    current_todos = todos[start:end]
    return current_todos

def autenticate():
    return

def create_app(test_config=None):
    app = Flask(__name__, template_folder='estacionamiento')
    setup_db(app)
    CORS(app, origins=['http://192.168.1.16:8080/'], max_age=10)    

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PATCH, DELETE')
        return response

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/carros', methods=['GET'])
    def get_carro():
        selection=Carro.query.order_by('id').all()
        carros=paginate(request, selection)
        if len(carros)==0:
            abort(404)
        return jsonify({
            'success':True,
            'carros':carros,
            'total_carros':len(carros)
        })
    
    @app.route('/carros', methods=['POST'])
    def create_carro():
        body=request.get_json()
        if body is None:
                abort(500)
        placa=body.get('placa', None)
        id_espacio=body.get('id_espacio', None)
        date=datetime.datetime.now()
        espacio=Espacio.query.filter(Espacio.id==id_espacio)
        if espacio.libre==False: 
            abort(500)
        espacio.libre=False
        espacio.update()
        try:
            carro=Carro(date=date, placa=placa, id_espacio=id_espacio)
            new_carro=carro.insert()
            selection=Carro.query.order_by('id').all()
            carros=paginate(request, selection)    
            return jsonify({
                'success':True,
                'created':new_carro,
                'carros':carros,
                'total_carros':len(carros)
            })

        except Exception as e:
            print(e)
            abort(500)
        
    @app.route('/carros/<carro_id>', methods=['DELETE'])
    def delete_carro_by_id(carro_id):
        error_404=False
        try:
            carro=Carro.query.filter(Carro.id==carro_id).one_or_none()
            if carro is None:
                error_404=True
                abort(404)
            pago=Pago(placa=carro.placa, monto=(datetime.datetime.now()-carro.date)*5)
            pago.insert()
            carro.delete()
            espacio=Espacio.query.filter(Espacio.id==carro.id_espacio)
            espacio.libre=True
            espacio.update()
            selection=Carro.query.order_by('id').all()
            carros=paginate(request, selection)
            return jsonify({
                'success':True,
                'deleted':carro_id,
                'carros':carros,
                'total_carros':len(carros)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/espacios', methods=['GET'])
    def get_espacio():
        selection=Espacio.query.order_by('id').all()
        espacios=paginate(request, selection)
        if len(espacios)==0:
            abort(404)
        return jsonify({
            'success':True,
            'espacios':espacios,
            'total_espacios':len(espacios)
        })
    

    
    @app.route('/pagos', methods=['GET'])
    def get_pago():
        selection=Pago.query.order_by('id').all()
        pagos=paginate(request, selection)
        if len(pagos)==0:
            abort(404)
        return jsonify({
            'success':True,
            'pagos':pagos,
            'total_pagos':len(pagos)
        })
    
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'code': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'internal server error'
        }), 500

    return app
