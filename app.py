from flask import Flask, request
from flask.ext.restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
import types


app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://opyate:passwd@db:5432/opyate'

test = {
        'spam': 'but I prefer bacon!',
        'eggs': 42,
        'obj': {'ham': 43, 'beans': 'with brandy!'}}

class MyModel(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    obj = db.Column('obj', JSONB, nullable=False)
    spam = db.Column('spam', db.String(length=256), nullable=False)
    eggs = db.Column('eggs', db.Integer(), nullable=False)


class Slash(Resource):
    def post(self):
        json = request.json
        assert(type(json) is types.DictType)
        exists = MyModel.query.filter_by(**request.json).first()
        if exists:
            return {'msg': 'payload exists'}, 409
        else:
            db.session.add(MyModel(**json))
            db.session.commit()
            return {'msg': 'payload created', 'payload': json}, 201

    def put(self):
        """
        call this to set up a test instance
        """
        db.session.add(MyModel(**test))
        db.session.commit()
        return {'msg': 'payload created', 'payload': test}


api.add_resource(Slash, '/')

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
