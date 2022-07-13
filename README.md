__Proyecto de desarrollo basado en plataformas__

__Docente:__ Marvin Abisrror Zarate

__Estacionamiento Utec__

__Integrantes:__

Hósmer Gilberto Casma Morales.

Sergio Marcelo Ricce Abregú.

Hans Alfonso Mendoza Alva.

Giancarlos Martell.


__Introducción__

El proyecto (Estacionamiento Utec) se basa en una plataforma virtual que permite crear usuarios, iniciar sesión y registrar en una base de datos los distintos carros en el servicio de estacionamiento Utec, mediante la placa de auto y el espacio en donde esté. Además el sistema registra automáticamente la hora de ingreso del vehículo. 


__Objetivo principal__

Nuestro objetivo es brindar un sistema seguro de registro eficaz, y de simple accesibilidad para que los usuarios del estacionamiento Utec puedan registrar de manera simple a los vehículos que usan el servicio. 

__Recursos empleados__

__Librerías :__

datetime

flask_sqlalchemy

flask_migrate

flask

flask_cors

flask_jwt_extended

__Framework :__

Flask

Psql

Vue.js


__API__

Insomnia REST : API REST que sirve para testeo

__/Request/responses:__

__/login__    methods = ['POST']

request : username, password.

return : jsonify({'success': False,'message': 'User not found'})
        
return : jsonify({'success': True,'token': access_token,'message': 'Logged in successfully'})

___/carros__    methods = ['GET']

query : all

return : jsonify({'success': True,'carros': carros, 'total_carros':len(carros)})

__/carros__     methods = ['POST']

request : placa, id_espacio

response : date, placa, id_espacio_estacionamiento

return : jsonify({'success':True,'created':new_carro,'carros':carros,'total_carros':len(carros)

__/carros/<carro_id>__     methods = ['DELETE']

query : carro_id

return : jsonify({'success':True,'deleted':carro_id,'carros':carros,'total_carros':len(carros)})

__/espacios__      methods = ['GET']

query : all()

return : jsonify({'success':True,'espacios':espacios,'total_espacios':len(espacios)})

__/pagos__     methods = ['GET']

query : all

return : jsonify({'success': True,'pagos': current_pagos,'total_pagos': len(pagos)})

__/pagos/<int:id>__     methods = ['GET']

query : id

return : jsonify({'success': True,'pago': pago.format()})

__/pagos__      methods = ['POST']

request : id, placa, monto

response : id, placa, monto

return : jsonify({'success': True,'pago': pago.format()})

__/usuarios__     methods = ['GET']

query : all

return : jsonify({'success': True,'administradores': paginate(request, usuarios),'total_administradores': len(usuarios)})

__/usuarios/<int:id>__    methods = ['GET']

query : id

return : jsonify({'success': True,'administrador': usuarios.format()})

__/usuarios__     methods = ['POST']

request : username, password

response : username, password

return : jsonify({'success': True,'administrador': usuario.format()})

__/usuarios/<int:id>__     methods = ['DELETE']

query : id

return : jsonify({'success': True,'delete': id})

___Hosts:__

http://127.0.0.1:8081
http://127.0.0.1:5000

localhost:8081

___Forma de autenticación:__

El login sirve para que un usuario pueda registrar los carros en el estacionamiento utec una vez creada su cuenta, debe brindar su nombre de usuario y contraseña. Con la ayuda de JSON Web Token, mejoramos la seguridad de la aplicación evitando la entrada a las cuentas por parte de gente no deseada, restrinjiendo la entrada a la gente que conoce los datos correctos.

___Manejo de errores:__

200: Se a aceptado el request exitosamente

302: Recurso solicitado ha sido movido temporalmente a la URL

400: Recurso mal solicitado

401: Petición no ejecutada por falta de autorización

404: Recurso no encontrado

405: Método a ejecutar no permitido

500: Error por fallo en la aplicación


__Ejecución del sistema__

Al momento de que el usuario ingrese al dominio, llegará a la página principal en donde tendrá las opciones de registrar o iniciar sesión de un usuario, para eventualmente tener acceso a la función principal del sistema, que es la gestión de autos del Estacionamiento Utec.