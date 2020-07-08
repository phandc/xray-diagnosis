# from flask_restful import Resource, Api, request
# from package.model import conn
#
#
# class User(Resource):
#
#
#
#
#
#         def post(self):
#             """api to add the patient in the database"""
#
#             userInput = request.get_json(force=True)
#             username1 = userInput['username']
#             password1 = userInput['password']
#             user = conn.execute("SELECT * FROM user WHERE username = ?", (username1,)).fetchall()
#             return user
#
