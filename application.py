from flask import Flask, render_template , redirect
# from flask_sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime
import json
from flask_mail import Mail
from flask import flash
from flask import Flask, render_template, request, url_for,session
from werkzeug.utils import redirect
from crud import CRUDOperations
from flask_session import Session
from flask_bcrypt import Bcrypt

import support

local_server = True
application= Flask(__name__, template_folder="Templates")
application.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USE_TSL=False,
    MAIL_USERNAME='rakherajas21@gmail.com',
    MAIL_PASSWORD='vit@19732020'
)
mail = Mail(application)


application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
application.secret_key="loginsession"
Session(application)


@application.route('/section')
def section():
    return render_template("sectionlist.html")


@application.route('/admin')
def admin():

    if not session.get('Name'):
        return redirect('/login')
    else:
        data=['section 1','section 2','section 3','section 4','section 5','section 6']
        data2=['subsection 1','subsection 2','subsection 3']
        return render_template('/Admin/sectionlist.html',data=data,data2=data2)

@application.route('/Form')
def Form():
    if not session.get('Name'):
        return redirect('/login')
    else:
        return render_template('/Admin/form.html')

@application.route('/login')
def form():
    return render_template('/Admin/disk.html')

@application.route('/logout')
def logout():
    session.pop('Name',None)
    return redirect('/')

@application.route('/error')
def display():
    return '<h1>incorrect credintials</h1>'

@application.route('/data', methods = ['POST', 'GET'])
def login():
    # hashed_password = bcrypt.generate_password_hash('admin123')

    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['Name']=username

        if(support.func(username,password)):
            return redirect("/admin")
        else:
            return redirect("/error")


@application.route("/")
def index():
    # obj_list = Competition.query.all()
    # obj_list1 = Count_no.query.all()
    # print(obj_list1)
    # obj_list.reverse()
    # return render_template("index.html",data=obj_list, count=obj_list1 )
    return render_template("index.html",data=[''], count=[''] )



@application.route("/about")
def about():
    return render_template("about.html")

@application.route("/competition_up")
def competition_up():
    obj_list = Competition.query.all()
    obj_list.reverse()
    return render_template("competition.html",data=obj_list)



@application.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        phone = request.form.get('phone')
        message = request.form.get('message')
        print(email)
        #entry = Contact(Name=name, Subjectt=subject, Phn_no=phone, Mail=email, Date=datetime.now(), Message=message)

        #db.session.add(entry)
        #db.session.commit()

        mail.send_message('New message from' + name,
                          sender='user07g@gmail.com',
                          recipients=['user07g@gmail.com'],
                          body=message + '\n' + phone
                          )

    return render_template("contact.html")


@application.route("/events")
def events():
    return render_template("events.html")

@application.route("/result")
def results():
    return render_template("results.html")


@application.route("/course_details")
def course_details():
    return render_template("course_details.html")


@application.route("/courses")
def courses():
    return render_template("courses.html")


@application.route("/abacus_d")
def abacus_d():
    return render_template("course-details/abacus-d.html")


@application.route("/vedic")
def vedic():
    return render_template("course-details/vedic.html")


@application.route("/phonics")
def phonics():
    return render_template("course-details/phonics.html")


@application.route("/rubic")
def rubic():
    return render_template("course-details/rubic.html")


@application.route("/kalfun")
def kalfun():
    return render_template("course-details/kalfun.html")


@application.route("/dmit")
def dmit():
    return render_template("course-details/dmit.html")

@application.route("/mont")
def mont():
    return render_template("course-details/mont.html")


@application.route("/Enroll Now" , methods=['GET', 'POST'])
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
                          sender='rakherajas21@gmail.com',
                          recipients=['rakherajas21@gmail.com'],
                          body= name + '\n' + email + '\n' + phone + '\n' + address + '\nCategory: ' + category + '\nCourse: ' + course + '\nComment: ' + comment
                          )

        mail.send_message('New message from MEGAMIND Institute',
                          sender='rakherajas21@gmail.com',
                          recipients=[email],
                          body="ThanK you for contacting US."
                          )

    return render_template("Enroll Now.html")


@application.route("/teacher training")
def t_training():
    return render_template("Teacher-Training.html")




@application.route("/admin" )
def ad_login(error=0):

    if error:
        error = "Invalid Password"
        return render_template("Admin/admin_login.html", error=error)
    else:
        return render_template("Admin/admin_login.html")



@application.route("/competition",  methods=['GET', 'POST'])
def admin_login():
    if (request.method == 'POST'):
        C_name = request.form.get('C_name')
        date=request.form.get('date')
        Url=request.form.get('Url')
        description= request.form.get('description')
        print(C_name,date,description)
        entry = Competition(C_name=C_name, date=date,Url=Url, description=description)

        db.session.add(entry)
        db.session.commit()
        print("Data added successfully")
    obj_list = Competition.query.all()
    obj_list.reverse()
    return render_template("Admin/admin.html",data=obj_list)\



@application.route('/view_entries')
def view_entries():
    items = CRUDOperations.get_all_items()
    return render_template('view_entries.html', items=items)


@application.route('/delete_entry/<id>', methods=['POST'])
def delete_entry(id):
    CRUDOperations.delete_item(id)
    return redirect(url_for('view_entries'))


@application.route('/update_entry/<id>', methods=['GET', 'POST'])
def update_entry(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        item = {
            'id': id,
            'title': title,
            'desc': desc
        }
        CRUDOperations.update_item(item)
        return redirect(url_for('view_entries'))

    # Retrieve the existing item
    items = CRUDOperations.get_all_items()
    item = next((item for item in items if item['id'] == id), None)
    if item is None:
        return "Item not found"

    return render_template('update_entry.html', item=item)


@application.route('/update_entry', methods=['POST'])
def update_entry_redirect():
    id = request.form['id']
    return redirect(url_for('update_entry', id=id))



if (__name__ == "__main__"):
    application.run(debug=True)
