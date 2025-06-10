from flask import Flask, request, render_template, jsonify, send_from_directory, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin
import json
import jwt
import datetime
import sqlite3
import uuid
import bcrypt
import base64
from io import BytesIO
from random_username.generate import generate_username
import DatabaseCreation
from functools import wraps
from imgUploader import *
from nudity import *
from emailSender import *

###############################################################################################
# DEVELOPEMENT
###############################################################################################

SECRET_KEY = 'SUPER_SECRET_PASSWORD'
PEPER = 'SUPER_SECRET_PEPER'
DOMAIN = "http://127.0.0.1:5000"
ADMIN_LIST = ["shantanubhargava2005@gmail.com","gamerzzden@gmail.com"]
DEBUG = True



###############################################################################################
# INITIALISATION
###############################################################################################

app = Flask(__name__)
CORS(app, support_credentials=True)
limiter = Limiter(
    get_remote_address,
    default_limits=["100 per minute"],
    app=app
)

###############################################################################################
# DATABASE SETUP
###############################################################################################

app.config['DATABASE'] = './MaskIT.db'

def get_db(fdrp=False):    
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    get_db().commit()
    return (rv[0] if rv else None) if one else rv

###############################################################################################
# JWT SETUP
###############################################################################################


def create_jwt_token(user_id):
    payload = {
        'sub': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Token expiration time
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return (payload['sub'])
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is invalid
    
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            user_id = verify_jwt_token(token)
            given_user_id = request.form.get('user_id')

            if user_id != given_user_id:
                return jsonify({'error': 'Unauthorized: User ID mismatch'}), 401

        except Exception as e:
            return jsonify({'error': f'Error verifying token: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
    
###############################################################################################
# SVELTE SETUP
###############################################################################################
    
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


###############################################################################################
# USER RELATED ENDPOINTS
###############################################################################################

@app.route("/Ping", methods=['POST'])
@limiter.limit("100 per minute")
def Ping():
    return "Pong"

@app.route("/SignUp", methods=['POST'])
@limiter.limit("10 per minute")
def SignUp():
    try:
        user_id = generate_username(1)[0]
        password = request.form.get('password')
        email = request.form.get('email')
        name = "PLACEHOLDER NAME"

        print(user_id, password, email, name)

        if email in ADMIN_LIST:
            isAdmin = True
        else:
            isAdmin = False

        
        d = query_db("SELECT * FROM USERS WHERE USER_ID COLLATE NOCASE = ?", (user_id,))
        if len(d) > 0:
            return {"UsernameError": "Username already registered"}
        
        d = query_db("SELECT * FROM USERS WHERE EMAIL COLLATE NOCASE = ?", (email,))
        if len(d) > 0:
            if not isAdmin:
                return {"EmailError": "Email already registered"}

        if not name and not DEBUG:
            return {"error": "Invalid Name"}
        if not user_id or any(c in '"!@#$%^&*()+\' ?=,<>/' for c in user_id):
            return {"error": "Invalid Username"}
        
        if (not email) or (not email.split("@")[-1].lower() in "learner.manipal.edu"):
            if not isAdmin:
                return {"EmailError": "Invalid email, are you from manipal?"}
        

        id_jwt = create_jwt_token(user_id)
        pass_jwt = create_jwt_token(password)
        email_jwt = create_jwt_token(email)
        name_jwt = create_jwt_token(name)

    
        query_db("INSERT INTO UNVERIFIED VALUES(?, ?, ?, ?)", (id_jwt, pass_jwt, email_jwt, name_jwt))
    
        link = f"{DOMAIN}/Verify?id_jwt={id_jwt}"

        if not DEBUG:
            if send_email([email], name, link):
                return {"message": "Verification Email has been sent!"}
            else:
                return {"error": "Something went wrong! Please try again"}
        else:
            print(link)
            return "Please check email"
        
    except Exception as e:
        return {"error": str(e)}


@app.route("/Verify", methods=['GET'])
def Verify():
    try:
        id_jwt = request.args.get('id_jwt')
        pass_jwt = request.args.get('pass_jwt')
        email_jwt = request.args.get('email_jwt')
        name_jwt = request.args.get('name_jwt')

        result = query_db("SELECT * FROM UNVERIFIED WHERE ID_JWT = ?",
                    (id_jwt,))

        if len(result) == 0:
            return "Verification failed, Unauthorized"
        else:
            result = result[0]
            user_id = verify_jwt_token(id_jwt)
            password = verify_jwt_token(result[1])
            email = verify_jwt_token(result[2])
            name = verify_jwt_token(result[3])
        
            hp = password + PEPER
            salt = bcrypt.gensalt()
            bts = hp.encode('utf-8')
            hashed = bcrypt.hashpw(bts, salt)
            
            query_db("INSERT INTO USERS VALUES (?, ?, ?, ?, ?, NULL, DATETIME('now'))",
                        (user_id, hashed, salt, name, email))
            
            query_db("DELETE FROM UNVERIFIED WHERE ID_JWT = ?", (id_jwt,))

            return "Verification successful"
    except Exception as e:
        return str(e)
        

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    email = request.form.get('email')
    password = request.form.get('password')


    query = "SELECT EMAIL, PASSWORD, SALT, USER_ID FROM USERS WHERE EMAIL = ?"
    result = query_db(query, (email,))
    
    if len(result) > 0 and bcrypt.hashpw((password+PEPER).encode("utf-8"), result[0][2]) == result[0][1]:

        token = create_jwt_token(result[0][3])
        return {'token': token}
    else:
        return {'error': 'Invalid credentials'}

    
###############################################################################################
# POST RELATED ENDPOINTS
###############################################################################################

@app.route('/GetPost', methods=['POST'])
@limiter.limit("180 per minute")
def GetPost():
    post_id = request.form.get("post_id")
    
    print(post_id)

    rows = query_db("SELECT * FROM POSTS WHERE POST_ID = ?", (post_id,))

    if len(rows) > 0:
        return jsonify(rows[0])
    else:
        return {"error": "Not found"}, 404
    
# Example curl command:
# curl --header "Authorization:TOKEN" \
# -F "data={\"user_id\": \"LOL\", \"caption\": \"ok\", \"tags\": \"ss\", \"location\": \"loc\"};type=application/json" \
# -F "image=@/home/hacker097/Desktop/dependency.png" http://localhost:5000/CreatePost

@app.route('/CreatePost', methods=['POST'])
@limiter.limit("6 per minute")
@token_required
def CreatePost():
    post_id = str(uuid.uuid4())

    
    caption = request.form.get('caption')
    tags = request.form.get('tags')
    location = request.form.get('location')
    body = request.form.get('body')
    user_id = request.form.get("user_id")


    try:
        if "image" not in request.files:
            print("OKOK")

            query_db("INSERT INTO POSTS VALUES (?, ?, ?, ?, ?, NULL, DATETIME('now'), 0, ?)",
                        (post_id, user_id, caption, tags, location, body))
            

        else:
            image_file = request.files['image']

            
            if image_file.filename == '':
                return jsonify({"error": "No selected image"}), 400

            temp_path = 'temp_upload.jpg'
            image_file.save(temp_path)


            #if nudityCheck(temp_path):
            #    return {"error": "No explicit imagery allowed"}
            
            imgur_link = ImageUploader(temp_path)


            query_db("INSERT INTO POSTS VALUES (?, ?, ?, ?, ?, ?, DATETIME('now'), 0, NULL)",
                        (post_id, user_id, caption, tags, location, imgur_link))

    except Exception as e:
            return {"error": e}, 500

            
    return {'message': 'Post successful'}, 200


@app.route('/EditPost', methods=['POST'])
@limiter.limit("12 per minute")
@token_required
def EditPost():
    try:

        post_id = request.form.get('post_id')
        caption = request.form.get('caption')
        tags = request.form.get('tags')
        location = request.form.get('location')
        
        query_db("UPDATE POSTS SET CAPTION = ?, tags = ?, LOCATION = ? WHERE POST_ID = ?",
                    (caption, tags, location, post_id))
            
        return {'message': 'Edit successful'}, 200

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/DeletePost', methods=['POST'])
@limiter.limit("180 per minute")
@token_required
def DeletePost():
    try:
        post_id = request.form.get('post_id')

        query_db("DELETE FROM POSTS WHERE POST_ID = ?", (post_id,))
            
        return {'message': 'Deletion successful'}, 200

    except Exception as e:
        return {"error": str(e)}, 500

    
###############################################################################################
# COMMENT RELATED ENDPOINTS
###############################################################################################

def build_comment_tree(comments, parent_id):
    comment_tree = []

    for comment in comments:
        if comment[5] == parent_id:
            comment_entry = {
                'COMMENT_ID': comment[0],
                'USER_ID': comment[1],
                'POST_ID': comment[2],
                'CREATED_TIME': comment[3],
                'COMMENT_TEXT': comment[4],
                'SCORE': comment[6],
                'REPLIES': build_comment_tree(comments, comment[0])
            }
            comment_tree.append(comment_entry)

    return comment_tree

@app.route('/GetCommentTree', methods=['POST'])
@limiter.limit("60 per minute")
def GetCommentTree():    
    post_id = request.form.get("post_id")

    all_comments = query_db("SELECT * FROM COMMENTS WHERE POST_ID = ? ORDER BY SCORE", (post_id,))

    comment_tree = build_comment_tree(all_comments, None)

    return jsonify(comment_tree)

    
@app.route('/CreateComment', methods=['POST'])
@limiter.limit("6 per minute")
@token_required
def CreateComment():
    try:

        post_id = request.form.get("post_id")
        user_id = request.form.get("user_id")
        text = request.form.get("text")
        reply_id = request.form.get("reply_id")
        comment_id = str(uuid.uuid4())

        if not reply_id:
            reply_id = None
        
        query_db("INSERT INTO COMMENTS VALUES (?, ?, ?, DATETIME('now'), ?, ?, 0)",
                    (comment_id, user_id, post_id, text, reply_id))

        comment = query_db("SELECT * FROM COMMENTS WHERE COMMENT_ID = ?", (comment_id,))[0]
        comment_entry = {
            'COMMENT_ID': comment[0],
            'USER_ID': comment[1],
            'POST_ID': comment[2],
            'CREATED_TIME': comment[3],
            'COMMENT_TEXT': comment[4],
            'SCORE': comment[6],
            'REPLIES': []
        }

        return jsonify(comment_entry)
    
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/EditComment', methods=['POST'])
@limiter.limit("12 per minute")
@token_required
def EditComment():
    try:

        comment_id = request.form.get('comment_id')
        comment_text = request.form.get('comment_text')
        

        query_db("UPDATE COMMENTS SET COMMENT_TEXT = ? WHERE COMMENT_ID = ?", (comment_text, comment_id))
            
        return {'message': 'Edit successful'}, 200

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/DeleteComment', methods=['POST'])
@limiter.limit("180 per minute")
@token_required
def DeleteComment():
    try:

        comment_id = request.form.get('comment_id')

        query_db("UPDATE COMMENTS SET COMMENT_TEXT = '[DELETED]', USER_ID = '[DELETED]' WHERE COMMENT_ID = ?",
                    (comment_id,))
            
        return {'message': 'Deletion successful'}, 200

    except Exception as e:
        return {"error": str(e)}, 500

    
###############################################################################################
# REACTION RELATED ENDPOINTS
###############################################################################################

@app.route('/ReactPost', methods=['POST'])
@limiter.limit("180 per minute")
@token_required
def ReactPost():
    try:
        post_id = request.form.get('post_id')
        user_id = request.form.get('user_id')
        reaction_type = int(request.form.get('reaction_type'))

        if abs(reaction_type) > 1:
            return {"error": "GET REKT NOOB"}

        result = query_db("SELECT * FROM REACTIONS WHERE POST_ID = ? AND TYPE = ? AND USER_ID = ?", (post_id, reaction_type, user_id))
        if len(result) > 0:
            return {"error": "Reaction already exists"}
        
        if reaction_type == 0:
            result = query_db("SELECT * FROM REACTIONS WHERE POST_ID = ? AND (TYPE = 1 OR TYPE = -1) AND USER_ID = ?", (post_id, user_id))
        else:
            result = query_db("SELECT * FROM REACTIONS WHERE POST_ID = ? AND (TYPE = ? OR TYPE = 0) AND USER_ID = ?", (post_id, reaction_type*-1, user_id))
        
        if len(result) == 0:
            query_db("INSERT INTO REACTIONS VALUES(?, ?, ?, NULL)", (reaction_type, user_id, post_id))
        else:
            query_db("UPDATE REACTIONS SET TYPE = ? WHERE USER_ID = ? AND POST_ID = ?", (reaction_type, user_id, post_id))
            
        query_db("UPDATE POSTS SET SCORE = (SELECT SUM(TYPE) FROM REACTIONS WHERE POST_ID = ?) WHERE POST_ID = ?", (post_id, post_id))
            

        return {"message": "Reaction successful"}
        
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/ReactComment', methods=['POST'])
@limiter.limit("180 per minute")
@token_required
def ReactComment():
    try:

        comment_id = request.form.get('comment_id')
        user_id = request.form.get('user_id')
        reaction_type = int(request.form.get('reaction_type'))

        if abs(reaction_type) > 1:
            return {"message": "GET REKT NOOB"}

        result = query_db("SELECT * FROM REACTIONS WHERE COMMENT_ID = ? AND TYPE = ? AND USER_ID = ?", (comment_id, reaction_type, user_id))
        if len(result) > 0:
            return {"error": "Reaction already exists"}
        
        if reaction_type == 0:
            result = query_db("SELECT * FROM REACTIONS WHERE COMMENT_ID = ? AND (TYPE = 1 OR TYPE = -1) AND USER_ID = ?", (comment_id, user_id))
        else:
            result = query_db("SELECT * FROM REACTIONS WHERE COMMENT_ID = ? AND (TYPE = ? OR TYPE = 0) AND USER_ID = ?", (comment_id, reaction_type*-1, user_id))
        
        if len(result) == 0:
            query_db("INSERT INTO REACTIONS VALUES(?, ?, NULL, ?)", (reaction_type, user_id, comment_id))
        else:
            query_db("UPDATE REACTIONS SET TYPE = ? WHERE USER_ID = ? AND COMMENT_ID = ?", (reaction_type, user_id, comment_id))
            
        query_db("UPDATE COMMENTS SET SCORE = (SELECT SUM(TYPE) FROM REACTIONS WHERE COMMENT_ID = ?) WHERE COMMENT_ID = ?",
                    (comment_id, comment_id))
            
        return {"message": "Reaction successful"}
        
    except Exception as e:
        return {"error": str(e)}, 500

###############################################################################################
# Feed related endpoints
###############################################################################################

@app.route('/GetFeed', methods=['POST'])
@limiter.limit("180 per minute")
def GetFeed():    
    return jsonify(query_db("SELECT * FROM POSTS ORDER BY (-SCORE)"))

###############################################################################################
# Profile related endpoints
###############################################################################################
    
@app.route('/GetProfile', methods=['POST'])
@limiter.limit("180 per minute")
def GetProfile():
    user_id = request.form.get('user_id')

    print(user_id)

    if(len(query_db("SELECT * FROM USERS WHERE USER_ID = ?", (user_id,))) == 0):
        return {"message": "Not found"}

    pc = query_db("SELECT COUNT() FROM POSTS WHERE USER_ID = ?", (user_id,))[0]
    cc = query_db("SELECT COUNT() FROM COMMENTS WHERE USER_ID = ?", (user_id,))[0]
    karma = query_db("SELECT SUM(TYPE) FROM REACTIONS WHERE USER_ID = ?", (user_id,))[0]
    

    return jsonify([pc, cc, karma])
    
###############################################################################################
# RUNNING THE APP
###############################################################################################

if __name__ == '__main__':
    app.run(debug=True)

