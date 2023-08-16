from flask import *
# from app import app
from flask_bcrypt import Bcrypt
# from flask import Flask,render_template, request,redirect
app = Flask(__name__)

bcrypt = Bcrypt(app)
def func(username,password):
    hashed_password = bcrypt.generate_password_hash('admin123')
    is_valid = bcrypt.check_password_hash(hashed_password, password)
    if username=="admin" and is_valid:
        return True
    else:
        return False



# {% for item in items %}
#                     <div class="course-info d-flex justify-content-between align-items-center">
#                         <h5>Title</h5>
#                         <p>{{ item['title'] }}</p>
#                     </div>
#                     <div class="course-info d-flex justify-content-between align-items-center">
#                         <h5>Description</h5>
#                         <p>{{ item['desc'] }}</p>
#                     </div>
#                 {% endfor %}

