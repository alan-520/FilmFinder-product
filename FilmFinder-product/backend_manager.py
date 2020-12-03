import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Resource, Api, fields, reqparse, inputs
from flask import Flask, request
import pymongo as pm
import json

client = pm.MongoClient('mongodb+srv://alan:123456unsw@alandb.yzqdi.mongodb.net/test')
db = client.main

app = Flask(__name__)
api = Api(app)
app.config['ERROR_404_HELP'] = False

parser1 = reqparse.RequestParser()
parser1.add_argument('movie_name', type=str, required=True)
parser1.add_argument('movie_type', type=str, required=True)
parser1.add_argument('actor', type=str, required=True)
parser1.add_argument('director', type=str, required=True)
parser1.add_argument('description', type=str, required=True)
parser1.add_argument('issue_date', type=str, required=True)

parser2 = reqparse.RequestParser()
parser2.add_argument('movie_type', type=str)
parser2.add_argument('actor', type=str)
parser2.add_argument('director', type=str)
parser2.add_argument('description', type=str)
parser2.add_argument('issue_date', type=str)

@api.route('/manager')
class manager(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found Error')
    @api.expect(parser1)
    @api.doc(description="Creat a new movie")
    def post(self):
        args = parser1.parse_args()
        movie_name = args.get('movie_name')
        movie_type = args.get('movie_type')
        actor = args.get('actor')
        director = args.get('director')
        description = args.get('description')
        issue_date = args.get('issue_date')
        data = {"movie_name": movie_name, "movie_type": movie_type, "actor": actor, "director": director,\
                "description": description, "issue_date": issue_date}
        try:
            db.movies.insert_one(data)
            return {"message": "created"}, 200
        except:
            return {"message": "Not created"}, 400

@api.route('/manager/<movie_name>')
@api.param('movie_name', 'movie_name')
class get_movies(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found Error')
    @api.doc(description="Query a movie")
    def get(self, movie_name):
        try:
            result = db.movies.find_one({"movie_name": movie_name})
            del result['_id']
            return result, 200
        except:
            return {"message": "Not Found"}, 404

@api.route('/manager/update/<movie_name>')
@api.param('movie_name', 'movie_name')
class Update_movie(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found Error')
    @api.expect(parser2)
    @api.doc(description="Update a movie")
    def put(self, movie_name):
        args = parser2.parse_args()
        movie_type = args.get('movie_type')
        actor = args.get('actor')
        director = args.get('director')
        description = args.get('description')
        issue_date = args.get('issue_date')
        try:
            if movie_type:
                db.movies.update_one({"movie_name": movie_name}, {"$set": { "movie_type": movie_type}})
            if actor:
                db.movies.update_one({"movie_name": movie_name}, {"$set": {"actor": actor}})
            if director:
                db.movies.update_one({"movie_name": movie_name}, {"$set": {"director": director}})
            if description:
                db.movies.update_one({"movie_name": movie_name}, {"$set": {"description": description}})
            if issue_date:
                db.movies.update_one({"movie_name": movie_name}, {"$set": {"issue_date": issue_date}})
            return {"message": "Updated"}, 200
        except:
            return {"message": "Not Updated"}, 400

@api.route('/manager/delete/<movie_name>')
@api.param('movie_name', 'movie_name')
class Delete_movie(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Not found Error')
    @api.doc(description="Delete a movie")
    def delete(self, movie_name):
        try:
            db.movies.delete_one({"movie_name": movie_name})
            return {"message": 'Deleted'}, 200
        except:
            return {"message": 'Not deleted'}, 400

if __name__ == "__main__":
    app.run('127.0.0.1', port=2222, debug=True)