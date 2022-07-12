from datetime import datetime
from flask import Flask, abort, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt_identity
from models import Usuario, setup_db, Carro, Espacio, Registro, Pago

TODOS_PER_PAGE=5

def paginate(request, seleccion):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*TODOS_PER_PAGE
    end = start + TODOS_PER_PAGE

    todos = [todo.format() for todo in seleccion]
    current_todos = todos[start:end]
    return current_todos

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, supports_credentials=True)
    cors = CORS(app, resources={r"http://localhost:8081/*": {"origins": "*"}})    

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PATCH, DELETE')
        return response

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = Usuario.query.filter_by(username=username, password=password).first()
        if user is None:
            return jsonify({
                'success': False,
                'message': 'User not found'
                 })
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'success': True,
            'token': access_token,
            'message': 'Logged in successfully'
        })
    
    @app.route('/carros', methods=['GET'])
    @jwt_required()
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
        date=datetime.now()
        espacio=Espacio.query.filter(Espacio.id==id_espacio)
        '''
        if espacio.libre==False: 
            abort(500)
        espacio.libre=False
        espacio.update()
        '''  
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
    @jwt_required()
    def get_pagos():
        pagos = Pago.query.all()
        current_pagos = paginate(request, pagos)
        return jsonify({
            'success': True,
            'pagos': current_pagos,
            'total_pagos': len(pagos)
        })
    
    @app.route('/pagos/<int:id>', methods=['GET'])
    def get_pago(id):
        pago = Pago.query.get(id)
        if pago is None:
            abort(404)
        return jsonify({
            'success': True,
            'pago': pago.format()
        })
    
    @app.route('/pagos', methods=['POST'])
    def create_pago():
        body = request.get_json()
        if not body:
            abort(400)
        pago = Pago(
            id = body['id'],
            placa = body['placa'],
            monto = body['monto'],
        )
        pago.insert()
        return jsonify({
            'success': True,
            'pago': pago.format()
        })
        
    @app.route('/usuarios', methods=['GET'])
    def get_usuarios():
        usuarios = Usuario.query.order_by('id').all()
        current_usuarios = paginate(request, usuarios)
        return jsonify({
            'success': True,
            'administradores': current_usuarios,
            'total_administradores': len(usuarios)
        })
    
    @app.route('/usuarios/<int:id>', methods=['GET'])
    def get_usuario(id):
        usuarios = Usuario.query.get(id)
        if usuarios is None:
            abort(404)
        return jsonify({
            'success': True,
            'administrador': usuarios.format()
        })
    
    @app.route('/usuarios', methods=['POST'])
    def create_usuario():
        body = request.get_json()
        if not body:
            abort(400)
        usuario = Usuario(
            username = body['username'],
            password = body['password']
        )
        usuario.insert()
        return jsonify({
            'success': True,
            'administrador': usuario.format()
        })
        
    @app.route('/usuarios/<int:id>', methods=['DELETE'])
    def delete_usuario(id):
        usuario=Usuario.query.get(id).one_or_none()
        if usuario is None:
            abort(404)
        usuario.delete()
        return jsonify({
            'success':True,
            'deleted_usuario':id
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
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)
