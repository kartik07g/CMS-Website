from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime
import json
from flask_mail import Mail

local_server = True
app = Flask(__name__, template_folder="Templates")
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USE_TSL=False,
    MAIL_USERNAME='user07g@gmail.com',
    MAIL_PASSWORD='k@rtik007'
)
mail = Mail(app)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@Localhost/contact_info'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@Localhost/contact_info'

db = SQLAlchemy(app)


class Contact(db.Model):
    Sr_No = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Subjectt = db.Column(db.String(100), nullable=False)
    Phn_no = db.Column(db.String(12), nullable=False)
    Date = db.Column(db.String(10), nullable=True)
    Mail = db.Column(db.String(50), nullable=False)
    Message = db.Column(db.String(300), nullable=False)


class Enroll(db.Model):
    Sr_No = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Phn_no = db.Column(db.String(12), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Address = db.Column(db.String(200), nullable=False)
    Comment = db.Column(db.String(300), nullable=False)
    Course=db.Column(db.String(20), nullable=False)
    Category = db.Column(db.String(20), nullable=False)

@app.route("/")
def index():
    return render_template("index.html", )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        phone = request.form.get('phone')
        message = request.form.get('message')

        print(email)
        entry = Contact(Name=name, Subjectt=subject, Phn_no=phone, Mail=email, Date=datetime.now(), Message=message)

        db.session.add(entry)
        db.session.commit()

        mail.send_message('New message from' + name,
                          sender='user07g@gmail.com',
                          recipients=['user07g@gmail.com'],
                          body=message + '\n' + phone
                          )

    return render_template("contact.html")


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/course_details")
def course_details():
    return render_template("course_details.html")


@app.route("/courses")
def courses():
    return render_template("courses.html")


@app.route("/abacus_d")
def abacus_d():
    return render_template("course-details/abacus-d.html")


@app.route("/vedic")
def vedic():
    return render_template("course-details/vedic.html")


@app.route("/phonics")
def phonics():
    return render_template("course-details/phonics.html")


@app.route("/rubic")
def rubic():
    return render_template("course-details/rubic.html")


@app.route("/kalfun")
def kalfun():
    return render_template("course-details/kalfun.html")


@app.route("/dmit")
def dmit():
    return render_template("course-details/dmit.html")


@app.route("/Enroll Now" , methods=['GET', 'POST'])
def enroll():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        category = request.form.get('category')
        course = request.form.get('course')
        comment = request.form.get('comment')
        entry = Enroll(Name=name, Email=email, Phn_no=phone, Address=address, Category=category, Course=course, Comment=comment)

        db.session.add(entry)
        db.session.commit()

        mail.send_message('New message from' + name,
                          sender='user07g@gmail.com',
                          recipients=['user07g@gmail.com'],
                          body= name + '\n' + email + '\n' + phone + '\n' + address + '\nCategory: ' + category + '\nCourse: ' + course + '\nComment: ' + comment
                          )
    return render_template("Enroll Now.html")


@app.route("/teacher training")
def t_training():
    return render_template("Teacher-Training.html")


if (__name__ == "__main__"):
    app.run(debug=True)
