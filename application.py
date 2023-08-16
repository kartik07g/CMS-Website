import os

import boto3
from flask import Flask, render_template, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime
import json
from flask_mail import Mail
from flask import flash
from flask import Flask, render_template, request, url_for, session
# from timestamp import timestamp
from werkzeug.utils import redirect
from register_crud import regist_operations
from crud import CRUDOperations
from form_crud import form_crud
from flask_session import Session
from flask_bcrypt import Bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import support
import random



# crud_instance = CRUDOperations()
# items = crud_instance.get_all_items()

# for item in items:
#     id_value = item['pass']
#     id_username = item['username']
#     print("pass:", id_value)
#     print("pass:", id_username)





local_server = True
application = Flask(__name__, template_folder="Templates")
# application.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL=True,
#     MAIL_USE_TSL=False,
#     MAIL_USERNAME='rakherajas21@gmail.com',
#     MAIL_PASSWORD='vit@19732020'
# )
# mail = Mail(application)

#my details

sender_email = 'pranit.das20@pccoepune.org'
sender_password = '120B10756'
receiver_email = 'pranitdas8@gmail.com'
# ,'kartik07g@gmail.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587




application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
application.secret_key = "loginsession"
Session(application)


@application.route('/section')
def section():
    return render_template("sectionlist.html")


@application.route('/admin')
def admin():
    if not session.get('Name'):
        return redirect('/')
    else:

        data = ['section 1', 'section 2', 'section 3', 'section 4', 'section 5', 'section 6']
        data2 = ['subsection 1', 'subsection 2', 'subsection 3']
        return render_template('/Admin/sectionlist.html', data=data, data2=data2)

        return render_template('/Admin/show.html', name=session['Name'])


@application.route('/Form')
def Form():
    return render_template('/Admin/form.html')


@application.route('/login')
def form():
    return render_template('/Admin/disk.html')


@application.route('/logout')
def logout():
    session.pop('Name', None)
    return redirect('/')


@application.route('/error')
def display():
    return '<h1>incorrect credintials</h1>'


@application.route('/data', methods=['POST', 'GET'])
def login():
    # hashed_password = bcrypt.generate_password_hash('admin123')

    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['Name'] = username

        if (support.func(username, password)):
            return redirect("/admin")

        if (support.func(username, password)):
            return redirect('/admin')

        else:
            return redirect("/error")


@application.route("/")
def index():
    # Retrieve the counts from the DynamoDB table

    # response = client.get_item(Key={'id': {'S': '1'}}, TableName='Count')
    # # counts = response.get('Item', {})
    # print(response['Item'])
    return render_template("index.html", data=[''], count=[''])

    # obj_list = Competition.query.all()
    # obj_list1 = Count_no.query.all()
    # print(obj_list1)
    # obj_list.reverse()
    # return render_template("index.html",data=obj_list, count=obj_list1 )


# return render_template("count.html", counts=counts)


@application.route("/about")
def about():
    table_name = 'division'
    crud_operations = CRUDOperations()
    div_items = crud_operations.get_all_items(table_name)
    count_items = crud_operations.get_all_items("Count")
    return render_template("about.html", div_items=div_items, count_items=count_items)


@application.route("/competition_up")
def competition_up():
    obj_list = Competition.query.all()
    obj_list.reverse()
    return render_template("competition.html", data=obj_list)


@application.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        topic = request.form.get('subject')
        phone = request.form.get('phone')
        message = request.form.get('message')
        # print(email)
        # entry = Contact(Name=name, Subjectt=subject, Phn_no=phone, Mail=email, Date=datetime.now(), Message=message)

        # db.session.add(entry)
        # db.session.commit()
        subject = 'Contact Us {} '.format(name)
        body = f"Dear Admin,\nI hope this email finds you well. My name is " \
               f"{name} and writing to inquire about your institute and here are my details\n" \
               f"Email: {email}\nPhone: {phone}\nSubject: {topic}\nMessage: {message}\nI " \
               f"have heard great things about your institute and believe it aligns with my goals and aspirations." \
               f" Could you please provide me with details regarding total cash required or any other documents you need from my side.\n\nI look forward to hearing from you at your earliest convenience. " \
               f"Thank you for your time and assistance.\n\nBest regards,\n{name}\n{phone}".format(name=name,
                                                                                                   email=email,
                                                                                                   phone=phone,
                                                                                                   subject=topic,
                                                                                                   message=message)

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)




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
    crud_operations = CRUDOperations()
    table_name = 'CMS-data'
    crud_operations.table_name=table_name
    items = crud_operations.get_all_items(table_name)
    return render_template("courses.html", items=items)


@application.route("/ADVANCE ABACUS")
def abacus_d():
    table_name = 'course-info'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)
    abacus_items = [item for item in items if item.get('course_name') == 'Advanced_abacus']
    return render_template("course-details/abacus-d.html", items=abacus_items)


@application.route("/INDIAN VEDIC MATHEMATICS")
def vedic():
    # table_name = 'course-info'
    # crud_operations = CRUDOperations()
    # crud_operations.table_name = table_name
    #
    # items = CRUDOperations().get_all_items()
    table_name = 'course-info'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)
    vedic_items = [item for item in items if item.get('course_name') == 'vedic']

    # for item in vedic_items:
    #     print("Title:", item['title'])
    #     print("Description:", item['desc'])
    #     print("\n")
    return render_template("course-details/vedic.html", items=vedic_items)


@application.route("/PHONICS")
def phonics():
    table_name = 'course-info'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)
    phonics_items = [item for item in items if item.get('course_name') == 'Phonics']
    return render_template("course-details/phonics.html", items=phonics_items)


@application.route("/RUBIC's CUBE")
def rubic():
    table_name = 'course-info'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)
    rubics_items = [item for item in items if item.get('course_name') == 'Rubics_cube']
    return render_template("course-details/rubic.html", items=rubics_items)


@application.route("/KALFUN")
def kalfun():
    table_name = 'course-info'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)
    kalfun_items = [item for item in items if item.get('course_name') == 'Kalfun']
    return render_template("course-details/kalfun.html", items=kalfun_items)


@application.route("/DMIT TEST")
def dmit():
    table_name = 'course-info'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)
    dmit_items = [item for item in items if item.get('course_name') == 'Dmit_test']
    return render_template("course-details/dmit.html", items=dmit_items)


@application.route("/MTT Course")
def mont():
    table_name = 'course-info'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)
    mtt_items = [item for item in items if item.get('course_name') == 'MTT']
    return render_template("course-details/mont.html", items=mtt_items)

@application.route("/competetion")
def competetion():
    table_name = 'events'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)
    comp_items = [item for item in items]
    return render_template("comp.html", items=comp_items)

@application.route("/Enroll_Now", methods=['GET', 'POST'])
def enroll():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        category = request.form.get('category')
        course = request.form.get('course')
        comment = request.form.get('comment')
        # entry = Enroll(Name=name, Email=email, Phn_no=phone, Address=address, Category=category, Course=course,
        #                Comment=comment)
        #
        # db.session.add(entry)
        # db.session.commit()
        item = {
            'id': {'N': '1'},
            'name': {'S': name},
            'email': {'S': email},
            'phone': {'N': phone},
            'address': {'S': address},
            'category': {'S': category},
            'course': {'S': course},
            'comment': {'S': comment}

        }
        regist_operations().add_item(item)

        # Prepare the email content
        subject = 'New Enrollment'
        body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}\nCategory: {category}\nCourse: {course}\nComment: {comment}"
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        return "Enrollment successful. You will receive a confirmation email shortly."



    return render_template("Enroll Now.html")


@application.route("/teacher training")
def t_training():
    return render_template("Teacher-Training.html")


@application.route("/admin")
def ad_login(error=0):
    if error:
        error = "Invalid Password"
        return render_template("Admin/admin_login.html", error=error)
    else:
        return render_template("Admin/admin_login.html")
@application.route("/enquiry", methods=['GET', 'POST'])
def enquiry():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        cash = request.form.get('cash')

        # Prepare the email content
        subject = 'New Enquiry from {} '.format(name)
        body = f"Dear Admin,\nI hope this email finds you well. My name is " \
               f"{name} and writing to inquire about your institute and here are my details\n" \
               f"Email: {email}\nPhone: {phone}\nAddress: {address}\nCash available to invest: {cash}\nI " \
               f"have heard great things about your institute and believe it aligns with my goals and aspirations." \
               f" Could you please provide me with details regarding total cash required or any other documents you need from my side.\n\nI look forward to hearing from you at your earliest convenience. " \
               f"Thank you for your time and assistance.\n\nBest regards,\n{name}\n{phone}".format(name=name,email=email,phone=phone,address=address,cash=cash)

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        # return "Enquiry sent successfully."

    return render_template("course-details/enquiry.html")

@application.route("/competition", methods=['GET', 'POST'])
def admin_login():
    if (request.method == 'POST'):
        C_name = request.form.get('C_name')
        date = request.form.get('date')
        Url = request.form.get('Url')
        description = request.form.get('description')
        print(C_name, date, description)
        entry = Competition(C_name=C_name, date=date, Url=Url, description=description)

        db.session.add(entry)
        db.session.commit()
        print("Data added successfully")
    obj_list = Competition.query.all()
    obj_list.reverse()
    return render_template("Admin/admin.html", data=obj_list) \
 \
        @ application.route("/count", methods=['GET', 'POST'])


def count():
    if (request.method == 'POST'):
        obj_list = Count_no.query.all()
        print(Count_no.Students)
        x = obj_list[0].Students
        str(x)
        if (Count_no.query.filter(Count_no.Students == x).delete()):
            print("done")

        Students = request.form.get('Stud_num')
        Courses = request.form.get('Courses_num')
        Events = request.form.get('Events_num')
        Trainers = request.form.get('Trainers_num')
        Franchise = request.form.get('Franchise_num')

        # Count_no.delete()
        # entry = Count_no(C_name=C_name, date=date,Url=Url, description=description)

    #     db.session.add(entry)
    #     db.session.commit()
    #     print("Data added successfully")
    # obj_list = Count_no.query.all()

    return render_template("Admin/admin.html", data=obj_list)


@application.route('/fill_div', methods=['GET', 'POST'])
def fill_div():
    table_name = 'division'  # Set the table name here

    crud_operations = CRUDOperations()  # Initialize the CRUDOperations instance

    random_number = random.randint(10000, 99999)
    random_number = str(random_number)
    if request.method == 'POST':
        name = request.form['name']
        post = request.form['post']
        city = request.form['city']
        contactnumber = request.form['contactnumber']
        item = {
            'id': {'N': random_number},
            'name': {'S': name},
            'post': {'S': post},
            'city': {'S': city},
            'contactnumber': {'N': contactnumber}
        }
        crud_operations.table_name = table_name  # Assign the table_name
        crud_operations.add_item(item)
        # return redirect(url_for('view_entries'))
    items = crud_operations.get_all_items(table_name)
    return render_template('fetch_division.html', items=items)

@application.route('/fill_events', methods=['GET', 'POST'])
def fill_events():
    table_name = 'events'  # Set the table name here
    crud_operations = CRUDOperations()
    random_number = random.randint(10000, 99999)
    random_number = str(random_number)
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        date = request.form['date']
        time = request.form['time']
        item = {
            'id': {'N': random_number},
            'title': {'S': title},
            'desc': {'S': desc},
            'date': {'S': date},
            'time': {'S': time}
        }
        crud_operations.table_name = table_name  # Assign the table_name
        crud_operations.add_item(item)
        # return redirect(url_for('view_entries'))
    items = crud_operations.get_all_items(table_name)
    return render_template('fetch_events.html', items=items)

@application.route('/view_events')
def view_events():
    table_name = 'events'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)  # Pass the table name as an argument
    return render_template('view_events.html', items=items)



@application.route('/delete_event/<id>', methods=['POST'])
def delete_event(id):
    crud_operations = CRUDOperations()
    crud_operations.table_name = 'events'
    crud_operations.delete_item(id)
    return redirect(url_for('fill_events'))

@application.route('/view_div')
def view_div():
    table_name = 'division'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)  # Pass the table name as an argument
    return render_template('view_division.html', items=items)



@application.route('/delete_div/<id>', methods=['POST'])
def delete_div(id):
    crud_operations = CRUDOperations()
    crud_operations.table_name = 'division'
    crud_operations.delete_item(id)
    return redirect(url_for('fill_div'))


@application.route('/fill_course', methods=['GET', 'POST'])
def fill_course():
    table_name = 'CMS-data'  # Set the table name here
    crud_operations = CRUDOperations()
    random_number = random.randint(10000, 99999)
    random_number = str(random_number)
    if request.method == 'POST':
        title = request.form['title']
        overview = request.form['overview']
        desc = request.form['desc']
        image = request.files['image']

        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Generate a unique filename
                filename = f"image_{str(hash(file))}.jpg"
        crud_operations.table_name = table_name
        s3_file_url = crud_operations.upload_image_to_s3(file.stream, filename)

        item = {
            'id': {'S': random_number},
            'title': {'S': title},
            'desc': {'S': desc},
            'overview': {'S': overview},
            'S3_file_url': {'S': s3_file_url if s3_file_url is not None else 'No Image'},
        }
        crud_operations.add_item(item)
    items = crud_operations.get_all_items(table_name)
    return render_template('fetch_course.html', items=items)




@application.route('/view_course')
def view_course():
    table_name = 'CMS-data'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)  # Pass the table name as an argument
    return render_template('view_course.html', items=items)

@application.route('/delete_course/<id>', methods=['POST'])
def delete_course(id):
    crud_operations = CRUDOperations()
    crud_operations.table_name = 'CMS-data'
    crud_operations.delete_itemm(id)
    return redirect(url_for('view_course'))

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
        CRUDOperations().update_item(item)
        return redirect(url_for('view_entries'))

    # Retrieve the existing item
    items = CRUDOperations().get_all_items()
    item = next((item for item in items if item['id'] == id), None)
    if item is None:

        return "Item not found"

    return render_template('update_entry.html', item=item)



@application.route('/fill_courseinfo', methods=['GET', 'POST'])
def fill_courseinfo():
    table_name = 'course-info'  # Set the table name here
    crud_operations = CRUDOperations()
    random_number = random.randint(10000, 99999)
    random_number = str(random_number)
    if request.method == 'POST':
        title = request.form['title']
        overview = request.form['overview']
        desc = request.form['desc']



        item = {
            'id': {'S': random_number},
            'title': {'S': title},
            'desc': {'S': desc},
            'overview': {'S': overview}
        }
        crud_operations.add_item(item)
    items = crud_operations.get_all_items(table_name)
    return render_template('fetch_courseinfo.html', items=items)


@application.route('/view_courseinfo')
def view_courseinfo():
    table_name = 'course-info'  # Set the table name
    crud_operations = CRUDOperations()
    items = crud_operations.get_all_items(table_name)  # Pass the table name as an argument
    return render_template('view_courseinfo.html', items=items)

@application.route('/update_entry', methods=['POST'])
def update_entry_redirect():
    id = request.form['id']
    return redirect(url_for('update_entry', id=id))


@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Generate a unique filename
                filename = f"image_{str(hash(file))}.jpg"
                #   Save the file to a temporary location on the server
                #  temp_filepath = r"C:\Users\navne\PycharmProjects\flask-tut\CMS_project\s3_images" + '\\' + filename
                #
                # file.save(temp_filepath)

                # Upload the file to S3 bucket
                crud = CRUDOperations()
                s3_file_url = crud.upload_image_to_s3(file.stream, filename)

                # Store the URL in DynamoDB
                item = {
                    'id': {'S': str(hash(file))},  # Use DynamoDB AttributeValue format
                    'title': {'S': 'image_title'},
                    'image_url': {'S': s3_file_url},
                    # 'timestamp': {'S': str(datetime.now())}
                }
                crud.add_item(item)
                crud.store_uploaded_image_url(str(hash(file)), s3_file_url)

                print("Image URL :", s3_file_url)

                return 'Image uploaded successfully'

        return 'No image selected or invalid file'

    return render_template('upload.html')


@application.route("/fill_count", methods=['GET', 'POST'])
def fill_count():
    table_name = 'Count'
    crud_operations = CRUDOperations()
    random_number = random.randint(10000, 99999)
    random_number_str = str(random_number)

    if request.method == 'POST':
        crud_operations.table_name = table_name
        crud_operations.delete_all_items()

        courses = request.form['courses']
        events = request.form['events']
        franchise = request.form['franchise']
        students = request.form['students']
        trainers = request.form['trainers']

        item = {
            'id': {'N': random_number_str},
            'courses': {'N': courses},
            'events': {'N': events},
            'franchise': {'N': franchise},
            'students': {'N': students},
            'trainers': {'N': trainers}
        }
        crud_operations.table_name = table_name
        crud_operations.add_item(item)

    items = crud_operations.get_all_items(table_name)
    return render_template('fetch_count.html', items=items)



# @application.route('/delete', methods=['GET', 'POST'])
# def delete():
#     if request.method == 'POST':
#         if 'filename' in request.form:
#             filename = request.form['filename']
#
#             # Delete the file from the S3 bucket
#             crud = CRUDOperations()
#             crud.delete_image_from_s3(filename)
#
#             return 'Image deleted successfully'
#
#         return 'No filename provided for deletion'
#
#     return render_template('delete.html')
# import boto3


@application.route('/newitems', methods=['GET', 'POST'])
def newitems():
    if request.method == 'POST':
        items = CRUDOperations().get_all_items()
        id = request.form['sections']
        title = request.form['section_name']
        desc = request.form['section_desc']
        item = {
            'id': {'S': id},
            'title': {'S': title},
            'desc': {'S': desc},
        }
        CRUDOperations().add_item(item)
        return redirect(url_for('view_division'))

    items = CRUDOperations().get_all_items()
    sections = [item['id'] for item in items]
    return render_template('/Admin/form.html', sections = sections)




# @application.route('/register', methods=['GET', 'POST'])
# def newitems():
#     if request.method == 'POST':
#         id = request.form['sections']
#         title = request.form['section_name']
#         desc = request.form['section_desc']
#
#
#         item = {
#             'id': {'S': id},
#             'title': {'S': title},
#             'desc': {'S': desc},
#         }
#         CRUDOperations().add_item(item)
#         # return redirect(url_for('view_entries'))
#     return render_template('/Admin/form.html')


@application.route('/section_name', methods=['GET', 'POST'])
def section_name():
    if request.method == 'POST':
        Section_name = request.form['Section_name']
        item = {
            'Section_name': {'S': Section_name}
        }
        form_crud().add_item(item)
        return redirect(url_for('view_division'))
    return render_template('fetch_division.html')

@application.route('/update_counts', methods=['POST'])
def update_counts():
    students = request.form['students']
    courses = request.form['courses']
    events = request.form['events']
    franchise = request.form['franchise']
    trainers = request.form['trainers']

    # Create an instance of the CRUDOperations class
    crud = CRUDOperations()
    # table_name = 'Count'
    # Update the counts in the DynamoDB table
    client.update_item(
        Key={'id': {'S': '1'}},
        UpdateExpression='SET students = :students, courses = :courses, events = :events, franchise = :franchise, trainers = :trainers',
        ExpressionAttributeValues={
            ':students': {'S': students},
            ':courses': {'S': courses},
            ':events': {'S': events},
            ':franchise': {'S': franchise},
            ':trainers': {'S': trainers}
        },
        # ConditionExpression='attribute_not_exists(id)',
        ReturnValues="ALL_NEW",  # Return the updated counts
        TableName='Count'
    )

    # Fetch the updated counts from the DynamoDB table
    # response = counts_table.get_item(Key={'id': 1})
    # counts = response['Item']  # Assuming the counts are stored in the 'Item' attribute
    # return response
    return redirect('/')


@application.route('/counts_form', methods=['GET'])
def counts_form():
    return render_template("fetch_count")

if (__name__ == "__main__"):
    application.run(debug=True)
