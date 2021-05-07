import datetime,bcrypt
from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
from dotenv import load_dotenv
import os
load_dotenv()

app=Flask(__name__)
client = MongoClient(os.getenv("MONGO_URL"))
db = client["database"]
user = db["user"]
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)
jwt = JWTManager(app)



@app.route("/register",methods=["POST"])
def register():
    
        email=request.json["email"]
        
        test=user.find_one({"email":email})
        
        if test:
            return jsonify(message="User Already Exist",status=409)
        else:

            password=request.json["password"]
            hashed=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            firstname=request.json["firstname"]
            lastname=request.json["lastname"]
            phone=request.json["phone"]
            user_input = {'firstname':firstname,'lastname':lastname,'phone':phone, 'email': email, 'password': hashed}
            user.insert_one(user_input)
          
            return jsonify(message="User created sucessfully.Please log in",status=200)


      
        
@app.route("/login",methods=["POST"])
def login():
        email=request.json["email"]
        password=request.json["password"]

        test=user.find_one({"email":email})
        
        if test:
            hashedpassword=test["password"]
            
            if bcrypt.checkpw(password.encode('utf-8'),hashedpassword):
                access_token = create_access_token(identity=email)
                return jsonify(message="Login Succeeded!", access_token=access_token,status=200)
                  
            else:
                return jsonify(message="Password is incorrect",status=409)


        else:
            return jsonify(message="User Doesn't Exist",status=409)


@app.route("/home",methods=["GET"])
@jwt_required()
def dasboard():
    return jsonify(message="Welcome to the home page !",status=200)



if __name__ == '__main__':
    app.run()
