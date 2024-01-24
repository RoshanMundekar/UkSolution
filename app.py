from flask import Flask,render_template,request,session, url_for, redirect, jsonify

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pymysql
from werkzeug.utils import secure_filename
import random
import os
import pathlib
from datetime import datetime
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 


def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="ukdb")
    return connection


def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")
        

con = dbConnection()
cursor = con.cursor()

app=Flask(__name__)



app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploaded_profile/'
app.config['UPLOADED_PHOTOS_DEST1'] = 'static/info/'
app.config['UPLOADED_PHOTOS_DEST2'] = 'static/youtube/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','wav','mp3'}
app.secret_key = 'any random string'

##################################################################################################################
                                                #mail code
##################################################################################################################
def sendemailtouser(usermail,ogpass):   
    fromaddr = "pranalibscproject@gmail.com"
    toaddr = usermail
   
    #instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = " MYCITYPEDIA.COM"
  
    # string to store the body of the mail 
    body = ogpass
  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication 
    s.login(fromaddr, "wkwfgosewcljcpqh") 
  
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
  
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
    # terminating the session 
    s.quit()
    


##################################################################################################################




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    username=session['user']
    image=session['image']
    email=session['email']
   
    return render_template('home.html',username=username,image=image,email=email)

@app.route('/about')
def about():
   
    return render_template("about.html")


##################################################################################################################
                                                #contact page
##################################################################################################################
@app.route('/contact', methods=["GET","POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        msg = request.form.get("msg")
        
        con = dbConnection()
        cursor = con.cursor()
        
        sql = "INSERT INTO stu_contact(Name, Email, Contact, Massage) VALUES (%s, %s, %s, %s)"
        val = (name, email, number, msg)
        cursor.execute(sql, val)
        con.commit()
      
        message = "Contact massage was successfully added by the user side.: " + name
        return jsonify({'message': message})
      
    return render_template('contact.html')


##################################################################################################################

@app.route('/logout')
def logout():
    session.pop('name',None)
    return render_template('index.html')
    # return redirect(url_for('index')) 



@app.route('/register')
def register():
    return render_template('register.html') 


##################################################################################################################
                                                #login
##################################################################################################################

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/login1',methods=['POST'])
def login1():
    if request.method == 'POST':
        Email = request.form.get("email")
        Password = request.form.get("password")
        print(Password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM stud_registration WHERE Stu_email = %s AND Stu_pass = %s', (Email, Password))
        print(result_count)
        
        if result_count == 1:
            res = cursor.fetchone()
            print(res)
            session['user'] = res[1]
            session['uid'] = res[0]
            session['image'] = res[7]
            session['email'] = res[2]
            # Successful login logic
            # return jsonify({'message': 'Login successful', 'user_id': res[0]})
            return "success"
        else:
            # Failed login logic
            # return jsonify({'message': 'Login failed'})
            return "fail"

        con.close()

##################################################################################################################
                                                #register
##################################################################################################################

@app.route('/get_otp', methods=['POST'])
def get_otp():
    if request.method =='POST':
        print("in record")
        details = request.form
        usermail = details['email']
        OTP = random.randint(1000, 9999)
        ogpass = "The uk solution verification tech successfully sent your OTP IS. "+ str(OTP)
        sendemailtouser(usermail,ogpass)
        return jsonify({'success': True, 'otp': OTP})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method =='POST':
        print("in record")
        details = request.form
        otp_entered = details['otp']
        otp_backend = details['otp1']
        print(otp_entered)
        print(otp_backend)
        
        if otp_entered == otp_backend:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
        


@app.route('/register1',methods=['POST'])
def register1():

    print("ouy")
    if request.method =='POST':
        print("in record")
        details = request.form
        Username = details['name']
        email = details['email']
        Mobile = details['mobile'] 
        Password = details['password']
        City = details['City'] 
        Address = details['Address']
        uploadimg = request.files['file']
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM stud_registration WHERE Stu_email = %s', (email))
        res = cursor.fetchone()
        # var password = "Abcdefg1";
        
        if not res:
           
            filename_secure = secure_filename(uploadimg.filename)
            uploadimg.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename_secure))
            filenamepath = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename_secure)
            
            
            sql = "INSERT INTO stud_registration(Stu_name, Stu_email, Stu_mobile, Stu_pass, Stu_city, Stu_address, Stu_image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (Username, email, Mobile, Password, City,Address,filenamepath)
            cursor.execute(sql, val)
            con.commit()
            
            sql1 = "INSERT INTO status(mailid) VALUES (%s)"
            val1 = (email,)
            cursor.execute(sql1, val1)
            con.commit()
        
            message = "Registration USER successfully added by USER side. Username: " + Username
            # return redirect(url_for('index'))
            return jsonify({'message': message})
            message = "Already available"
            
        else:
            message = "Please try Again ! " + Username
            dbClose()
            # return redirect(url_for('index'))
            return jsonify({'message': message})
        
            

##################################################################################################################






@app.route('/playlist/<id>')
def playlist(id):
    print(id)
    username=session['user']
    image=session['image']
    email=session['email']
    
    con = dbConnection()
    cursor = con.cursor()

   # Fetch data from the 'info' table
    cursor.execute('SELECT * FROM info WHERE ID = %s', (id))
    data = cursor.fetchone()

   # Fetch additional data if needed (adjust the query accordingly)
    cursor.execute('SELECT * FROM steps WHERE dropdown1 = %s', (id))
    data1 = cursor.fetchall()

    con.close()
     
    return render_template('playlist.html',username=username,image=image,email=email,data=data,data1=data1)


@app.route('/profile')
def profile():
    username=session['user']
    image=session['image']
    email=session['email']
    cursor.execute('SELECT * FROM stud_registration WHERE Stu_email = %s', (email))
    data = cursor.fetchone()
    
    cursor.execute('SELECT * FROM status WHERE mailid = %s', (email))
    data1 = cursor.fetchone()
    
    
    return render_template('profile.html',username=username,image=image,email=email,data=data,data1=data1)

@app.route('/teacher_profile')
def teacher_profile():
    return render_template('teacher_profile.html')


@app.route('/teachers')
def teachers():
    username=session['user']
    image=session['image']
    email=session['email']
    return render_template('teachers.html',username=username,image=image,email=email)


@app.route('/teachers1')
def teachers1():
    username=session['user']
    image=session['image']
    email=session['email']
    return render_template('teachers1.html',username=username,image=image,email=email)


@app.route('/teachers2')
def teachers2():
    username=session['user']
    image=session['image']
    email=session['email']
    return render_template('teachers2.html',username=username,image=image,email=email)



@app.route('/teachers3')
def teachers3():
    username=session['user']
    image=session['image']
    email=session['email']
    return render_template('teachers3.html',username=username,image=image,email=email)


@app.route('/teachers4')
def teachers4():
    username=session['user']
    image=session['image']
    email=session['email']
    return render_template('teachers4.html',username=username,image=image,email=email)


@app.route('/update', methods=["GET","POST"])
def update():
  
    username=session['user']
    image=session['image']
    email=session['email']
    
    return render_template('update.html',username=username,image=image,email=email)

@app.route('/update1', methods=['POST'])
def update1():
    id1=session['uid']
    print(id1)
    if request.method =='POST':
        print("in record")
        details = request.form
        Username = details['name']
        email = details['email']
        mobile = details['mobile']
        Password = details['old_pass'] 
        Address = details['Address']
        uploadimg = request.files['file']
        print("--")
        
        filename_secure = secure_filename(uploadimg.filename)
        uploadimg.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename_secure))
        filenamepath = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename_secure)
        
        
        # Update query with placeholders for column names
        update_query = "UPDATE stud_registration SET Stu_name = %s, Stu_email = %s, Stu_mobile = %s, Stu_pass = %s, Stu_address = %s, Stu_image = %s WHERE Id = %s"

        # Execute the update query
        cursor.execute(update_query, (Username, email, mobile, Password, Address, filenamepath, id1))
        print("----------")
        # Commit the changes and close the connection
        con.commit()
        con.close()
        
        message = "update USER successfully !"
      
        return jsonify({'message': message})
        
        
        
        

@app.route('/watchvideo/<id>')
def watchvideo(id):
    username=session['user']
    image=session['image']
    email=session['email']
   
    
    print(id)
    cursor.execute('SELECT * FROM steps WHERE id = %s', (id))
    data = cursor.fetchone()
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return render_template('watchvideo.html',data=data,username=username,image=image,email=email,formatted_datetime=formatted_datetime)

@app.route('/courses',methods=['POST','GET'])
def courses():
    username=session['user']
    image=session['image']
    email=session['email']
    
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM info')
    data = cursor.fetchall()
    return render_template('courses.html',username=username,image=image,email=email,data=data)

@app.route('/admin')
def admin():
    return render_template('adminlogin.html')
@app.route('/adhome')
def adhome():
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT ID,TITLE FROM info')
    data = cursor.fetchall()
    return render_template('adhome.html',data=data)


@app.route('/SessionHandle1',methods=['POST','GET'])
def SessionHandle1():
    if request.method == "POST":
        details = request.form
        name1 = details['name']
        session['name1'] = name1
        strofuser = name1
        print (strofuser.encode('utf8', 'ignore'))
        return strofuser    

@app.route('/submit_form',methods=['POST','GET'])
def submit_form():
    if request.method == "POST":
        name= request.form['name']
        email= request.form['email']
        number= request.form['number']
        msg= request.form['msg']
        uploadimg=request.files['file']
        
   
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM info WHERE EMAIL = %s', (email))
        res = cursor.fetchone()
        
        
        if not res:
           
            filename_secure = secure_filename(uploadimg.filename)
            uploadimg.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST1'], filename_secure))
            filenamepath = os.path.join(app.config['UPLOADED_PHOTOS_DEST1'], filename_secure)
            
            
            sql = "INSERT INTO info(TITLE, EMAIL, PHONE, MASSAGE, FILEIMAGE) VALUES (%s, %s, %s, %s, %s)"
            val = (name, email, number, msg, filenamepath)
            cursor.execute(sql, val)
            con.commit()
    
           
            return jsonify({'message': 'Form submitted successfully'})
              
        else:
            
            dbClose()
            return jsonify({'message': 'Please try Again !'})
        
        
        
        # print(file)
        # filename_secure = secure_filename(file.filename)
        # pathlib.Path(app.config['UPLOAD_FOLDER'], name).mkdir(exist_ok=True)
        # print("print saved")
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], name, filename_secure))
        # filename1 = os.path.join(app.config['UPLOAD_FOLDER'], name, filename_secure)        
    
@app.route('/submit_form1',methods=['POST','GET'])
def submit_form1():
    if request.method == "POST":
        uploadimg2=request.files['file2']
        name1= request.form['name1']
        dropdown1= request.form['dropdown1']
        msg1= request.form['msg1']
      
        uploadimg=request.files['file1']
        
        filename_secure1 = secure_filename(uploadimg2.filename)
        pathlib.Path(app.config['UPLOADED_PHOTOS_DEST2'], dropdown1).mkdir(exist_ok=True)
                       
        uploadimg2.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST2'], dropdown1, filename_secure1))
        filename2 = os.path.join(app.config['UPLOADED_PHOTOS_DEST2'], dropdown1, filename_secure1)
        
        
      
        filename_secure = secure_filename(uploadimg.filename)
        pathlib.Path(app.config['UPLOADED_PHOTOS_DEST2'], dropdown1).mkdir(exist_ok=True)
                       
        uploadimg.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST2'], dropdown1, filename_secure))
        filename1 = os.path.join(app.config['UPLOADED_PHOTOS_DEST2'], dropdown1, filename_secure)  
        
        sql = "INSERT INTO steps(stepname, dropdown1, msg1, uploadvideo,uploadimage) VALUES (%s, %s, %s, %s, %s)"
        val = (name1, dropdown1, msg1,filename1,filename2)
        cursor.execute(sql, val)
        con.commit()

       
        return jsonify({'message': 'Steps Form submitted successfully'})
    
    
    
              
@app.route('/update_status', methods=['POST'])
def update_status():
    email=session['email']
    try:
        # Update the status in the MySQL database
        with con.cursor() as cursor:
            # Assuming you have a table named 'your_table' with columns 'status' and 'id'
           sql = "UPDATE status SET BR = 'DONE' WHERE BR = 'PENDING' AND mailid = %s LIMIT 1"
           cursor.execute(sql, (email,))
           con.commit()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
              
@app.route('/update_status1', methods=['POST'])
def update_status1():
    email=session['email']
    try:
        # Update the status in the MySQL database
        with con.cursor() as cursor:
            # Assuming you have a table named 'your_table' with columns 'status' and 'id'
            sql = "UPDATE status SET BANK = 'DONE' WHERE BANK = 'PENDING' AND mailid = %s LIMIT 1"
            cursor.execute(sql, (email,))
            con.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
    
                  
@app.route('/update_status2', methods=['POST'])
def update_status2():
    email=session['email']
    try:
        # Update the status in the MySQL database
        with con.cursor() as cursor:
            # Assuming you have a table named 'your_table' with columns 'status' and 'id'
            sql = "UPDATE status SET NI = 'DONE' WHERE NI = 'PENDING' AND mailid = %s LIMIT 1"
            cursor.execute(sql, (email,))
            con.commit()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
@app.route('/update_status3', methods=['POST'])
def update_status3():
    email=session['email']
    try:
        # Update the status in the MySQL database
        with con.cursor() as cursor:
            # Assuming you have a table named 'your_table' with columns 'status' and 'id'
           sql = "UPDATE status SET GP = 'DONE' WHERE GP = 'PENDING' AND mailid = %s LIMIT 1"
           cursor.execute(sql, (email,))
           con.commit()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


    
if __name__=="__main__":
    app.run("0.0.0.0")
    # app.run(debug=True)