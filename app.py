from flask import Flask, request, jsonify, abort
from models import setup_db, User, Record
from flask_cors import CORS
import sys

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, DELETE , POST, PATCH')
        return response

    #----GET ENPOINTS----

    @app.route('/users', methods=['GET'])
    def get_users():
        try:
            user = User.query.all()
            formatted_users = [user.format() for user in user]
        
        except ValueError as e:
            print(e)
            abort(e)
        
        return jsonify({
            'success': True,
            'users': formatted_users
        })

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        print(user_id, file=sys.stderr)
        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
           abort()
        
        try:
            data=[]
            if len(user.records):
                formatted_records = [record.format() for record in user.records]
                data.append({
                    'user': user.format(),
                    'records': formatted_records
                })
            else:
                data.append({
                    'user': user.format(),
                })
        except ValueError as e:
            print(e)

        return jsonify({
            'success': True,
            'user': data
        })
        
    @app.route('/records', methods=['GET'])
    def get_records():
        try:
            record = Record.query.all()
            formatted_records = [record.format() for record in record]

        except ValueError as e:
            print(e)
            abort(e)
        
        return jsonify({
            'success': True,
            'records': formatted_records,
            })

    #----POST ENDPOINTS----

    @app.route('/users/create', methods=['POST'])
    def create_user():
        try:
            res = request.get_json()
            print(res)
            user = User(
                age = res['age'],
                email = res['email'],
                feet = res['feet'],
                inches = res['inches'],
                sex = res['sex'],
                user_name = res['user_name'],
                weight = res['weight'],
                weight_units = res['weight_units']
            )
            user.insert()

        except ValueError as e:
            print(e)
        
        return jsonify({
            'success': True,
            'user': user.id,
        })

    @app.route('/records/create', methods=['POST'])
    def create_record():
        try:
            res = request.get_json()
            record = Record(
                exercise = res['exercise'],
                reps = res['reps'],
                rest = res['rest'],
                weight = res['weight'],
                weight_units = res['weight_units'],
                user_id = res['user_id'],
            )
            record.insert()
        
        except ValueError as e:
            print(e)

        return jsonify({
            'success': True,
            'record': record.id
        })

    #----PATCH ENDPOINTS----

    @app.route('/records/<int:record_id>', methods=['PATCH'])
    def update_record(record_id):
        res = request.get_json()
        record = Record.query.filter(
            Record.id == record_id
        ).one_or_none()
        if record is None:
            abort('no record with that id')
        
        try:
            record.reps = res['reps']
            record.rest = res['rest']
            record.weight = res['weight']
            record.weight_units = res['weight_units']
            
            record.update()

        except ValueError as e:
            print(e)
        
        return jsonify({
            'success': True,
            'record': record.format() 
        })
    
    @app.route('/users/<int:user_id>', methods=['PATCH'])
    def update_user(user_id):
        res = request.get_json()
        user = User.query.filter(
            User.id == user_id
        ).one_or_none()
        
        if user is None:
            abort('no user with that id')
        try:
            user.age = res['age']
            user.feet = res['feet']
            user.inches = res['inches']
            user.user_name = res['user_name']
            user.weight = res['weight']
            user.weight_units = res['weight_units']

            user.update()

        except ValueError as e:
            print(e)

        return jsonify({
            'success': True,
            'user': user.format()
        })
        
    #----DELETE ENDPOINTS----

    @app.route('/records/delete/<int:record_id>', methods=['DELETE'])
    def delete_record(record_id):
        record = Record.query.filter(Record.id == record_id).one_or_none()
        if record is None:
            abort('no record with this id')
        try:
            record.delete()
        
        except ValueError as e:
            print(e)
        
        return jsonify({
            'success': True,
            'record_deleted': record.id,
        })
        
    return app
app = create_app()

if __name__ == '__main__':
    app.run()