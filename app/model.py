from flask import Flask, render_template, request, url_for, redirect
from app import app
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash, check_password_hash
#from bs4 import BeautifulSoup


from random import randint
  

#mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ankita@18Riya'
app.config['MYSQL_DB'] = 'ncdpython'


mysql = MySQL(app)

def final_touch(field):
    field = field.strip()
    field = field.replace("\\", "")
    #field = BeautifulSoup(field, convertEntities=BeautifulSoup.HTML_ENTITIES)
    return field 

@property
def password(self):
    raise AssertionError("Password is not a readable attribute!")

@password.setter
def password(self,password):
    password_hash=""
    self.password_hash=generate_password_hash(password)
    return password_hash

def verify_password(self,password):
    return check_password_hash(password_hash)

@app.route('/signup',methods=['GET', 'POST'])
def signup():
        
        error_fullname=error_email=error_password=""
        error_display_fullname=error_display_email=error_display_password="none"
        flag_error=0
        encrpt_pw=""

        if request.method=="POST":
            

            fullname=""
            email=""
            password=""
            repeatpw=""

            msg = " "
            
            fullname=request.form['fullname']
            fullname.capitalize()
            email=request.form['email']
            email.lower()
            password=request.form['password']
            repeatpw=request.form['repeatpassword']
            
            
            if(not fullname): 
                flag_error=1
                return render_template('index.html',error_display_fullname="block",
                        error_fullname="Error: Full Name is required")
            else:
                fullname = final_touch(fullname)
                if(fullname.isspace()):
                    flag_error=1
                    return render_template('index.html',error_display_fullname="block",
                            error_fullname="Error: Full Name can't start with a SPACE")

            if(not email): 
                flag_error=1
                return render_template('index.html',error_display_email="block",
                        error_email="Error: Full Name is required")
            else:
                email = final_touch(email)
                if(email.isspace()):
                    flag_error=1
                    return render_template('index.html',error_display_email="block",
                            error_email="Error: Full Name can't start with a SPACE")
            
            if(not password): 
                flag_error=1
                return render_template('registration.html',error_display_password="block",
                        error_password="Error: Password is required")
            else:
                password = final_touch(password)
                if(len(password)<8):
                    flag_error=1
                    return render_template('index.html',error_display_password="block",
                        error_password="Error: Password must be 8 characters long")
                else:
                    if(not repeatpw):
                        flag_error=1
                        return render_template('index.html',error_display_password="block",
                        error_password="Error: Password doesn't match")
                    else:
                        repeatpw = final_touch(repeatpw)
                        if(password == repeatpw):
                            encrpt_pw=password(password)
                        else:
                            flag_error=1
                            return render_template('index.html',error_display_lastname="block",
                            error_password="Error: Password doesn't match")
            
            if(flag_error==0):
                error_display_fullname=error_display_email=error_display_password="none"
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT email from patient')
                emailid=list(cursor.fetchall())
                cursor.close()
                print(emailid)
                print(type(emailid))

                if(len(emailid)>0):
                    for j in emailid:
                        if j.get('email')==email:
                            return render_template('registration.html',error="Error : Already a registered email id ") 
                        else: 
                            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                            cursor.execute('INSERT INTO login VALUES (Null,%s, % s, % s)',(fullname, email, password))
                            mysql.connection.commit()
                            msg='You have successfully registered !'
            
                else:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO login VALUES (Null,%s, % s, % s)',(fullname, email, password))
                    mysql.connection.commit()
                    msg='You have successfully registered !'

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT full_name from login WHERE email=%s',[email])
        full_name= cursor.fetchone()
        making_global_patient(full_name.get('full_name'))
        return render_template('home.html',full_name.get('full_name'))

@app.route('/search',methods=['GET', 'POST'])
def search():
    
    pk=""
    pid=""
    records=()
    
    if request.method=="POST":

        choice=request.form['choice']
        
        pk=request.form['pk']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if choice=='PATIENT ID':
            if(not pk):
                return render_template('search.html',error_display_patient_id="block",
                error_patient_id="Error: Patient ID is required")
            else:
                final_touch(pk)
                if(pk.isspace()):
                    return render_template('search.html',error_display_patient_id="block",
                        error_patient_id="Error: Patient ID doesn't start with a SPACE")
                
                if(len(pk)>14):
                    return render_template('search.html',error_display_patient_id="block",
                    error_patient_id="Error: Patient ID must be less than 14 digits")

                else:
                    pk = final_touch(pk)
                    if pk.isdigit():
                        cursor.execute("SELECT * from patient WHERE patient_id LIKE '%"+pk+"%' ;")
                        records=cursor.fetchall()
                        cursor.close()
                    else :
                        return render_template('search.html',error="Enter digits only") 
        elif choice=='C':
            pk.capitalize()
            if(not pk): 
                return render_template('search.html',error_display_firstname="block",
                    error_pk="Error: First Name is required")
            else:
                final_touch(pk)
                if(pk.isspace()):
                    return render_template('search.html',error_display_firstname="block",
                        error_firstname="Error: First Name doesn't start with a SPACE")
                else:
                    pk = final_touch(pk)
                    if (re.match('^[a-zA-Z\s]+$', pk)):
                        cursor.execute("SELECT * from patient WHERE first_name LIKE '%"+pk+"%' ;")
                        records=cursor.fetchall()
                        cursor.close()
                    else:
                        return render_template('search.html',error="Enter alphabets only") 

        elif choice=='LAST NAME':
            pk.capitalize()
            if(not pk): 
                return render_template('search.html',error_display_lastname="block",
                    error_lastname="Error: First Name is required")
            else:
                final_touch(pk)
                if(pk.isspace()):
                    return render_template('search.html',error_display_lastname="block",
                        error_lastname="Error: Last Name doesn't start with a SPACE")
                else:
                    pk = final_touch(pk)
                    if (re.match('^[a-zA-Z\s]+$', pk)):
                        cursor.execute("SELECT * from patient WHERE last_name LIKE '%"+pk+"%' ;")
                        records=cursor.fetchall()
                        cursor.close()
                    else:
                        return render_template('search.html',error="Enter alphabets only") 

    return render_template('search.html', records=records)

@app.route('/alldata',methods=['GET', 'POST'])
def alldata():
    if request.method=="POST":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from patient;")
        records=cursor.fetchall()
        cursor.close()
    return render_template('search.html', records=records)

def making_global_aadhaar(aadh):
    global aadhaar
    aadhaar=aadh
    
def making_global_patient(patientid):
    global patient_id
    patient_id = patientid

@app.route('/register', methods=['GET', 'POST'])
def register():


    error_firstname=error_lastname=error_gender=error_aadhaar=error_phone=error_dob=error_pincode=error_head=""
    error_display_firstname=error_display_lastname=error_display_gender=error_display_aadhaar =error_display_phone=error_display_pincode=error_display_dob=error_display_head="none"
    flag_error=0
    if request.method=="POST":

        firstname=""
        lastname=""
        gender=""
        aadhaar=""
        phone=""
        birthday=""
        pincode=""
        total=0
        screening=""
        msg = " "
        patient_id=""

        
        firstname=request.form['firstname']
        firstname.capitalize()
        lastname=request.form['lastname']
        lastname.capitalize()
        gender=request.form['gender']
        aadhaar=request.form['aadhaar']
        phone=request.form['phone']
        birthday=request.form['birthday']
        pincode=request.form['pincode']
        
        if(not firstname): 
            flag_error=1
            return render_template('registration.html',error_display_firstname="block",
                    error_firstname="Error: First Name is required",lastname=lastname,gender=gender,aadhaar=aadhaar,
                    phone=phone,birthday=birthday,pincode=pincode)
        else:
            final_touch(firstname)
            if(firstname.isspace()):
                flag_error=1
                return render_template('registration.html',error_display_firstname="block",
                        error_firstname="Error: First Name can't start with a SPACE",lastname=lastname,gender=gender,
                        aadhaar=aadhaar,phone=phone,birthday=birthday,pincode=pincode)

        
        if(not lastname): 
            flag_error=1
            return render_template('registration.html',error_display_lastname="block",
                    error_lastname="Error: Last Name is required",firstname=firstname,gender=gender,aadhaar=aadhaar,
                    phone=phone,birthday=birthday,pincode=pincode)
        else:
            final_touch(lastname)
            if(lastname.isspace()):
                flag_error=1
                return render_template('registration.html',error_display_lastname="block",
                        error_lastname="Error: Last Name can't start with a SPACE",firstname=firstname,gender=gender,
                        aadhaar=aadhaar,phone=phone,birthday=birthday,pincode=pincode)

        
        if(not gender):
            flag_error=1
            return render_template('registration.html',error_display_gender="block",
                    error_gender="Error: Select your gender",
                    firstname=firstname,lastname=lastname,aadhaar=aadhaar,phone=phone,birthday=birthday,pincode=pincode)
        else:
            gender = final_touch(gender)
	
        
        if(not aadhaar):
            flag_error=1
            return render_template('registration.html',error_display_aadhaar="block",
                    error_aadhaar="Error: Aadhaar UID is required",
                    firstname=firstname,lastname=lastname,gender=gender,phone=phone,birthday=birthday,pincode=pincode)
        else:
            aadhaar = final_touch(aadhaar)
            if(len(aadhaar)<12):
                flag_error=1
                return render_template('registration.html',error_display_aadhaar="block",
                    error_aadhaar="Error: Aadhaar UID must be 12 digits long",
                    firstname=firstname,lastname=lastname,gender=gender,phone=phone,birthday=birthday,pincode=pincode)

        
        if(not phone):
            flag_error=1
            return render_template('registration.html',error_display_phone="block",
                    error_phone="Error: Phone No. is required",
                    firstname=firstname,lastname=lastname,gender=gender,aadhaar=aadhaar,birthday=birthday,pincode=pincode)
        else:
            phone = final_touch(phone)
            if(len(phone)<10):
                flag_error=1
                return render_template('registration.html',error_display_phone="block",
                    error_phone="Error: Phone No. must be 10 digits long",
                    firstname=firstname,lastname=lastname,gender=gender,aadhaar=aadhaar,birthday=birthday,pincode=pincode)

        
        if(not birthday):
            flag_error=1
            return render_template('registration.html',error_display_dob="block",
                    error_dob="Error: Date fo Birth is required",
                    firstname=firstname,lastname=lastname,gender=gender,aadhaar=aadhaar,phone=phone,pincode=pincode)
        else:
            birthday = final_touch(birthday)

        
        if(not pincode):
            flag_error=1
            return render_template('registration.html',error_display_pincode="block",
                    error_pincode="Error: Pincode. is required",
                    firstname=firstname,lastname=lastname,gender=gender,aadhaar=aadhaar,phone=phone,birthday=birthday)
        else:
            pincode = final_touch(pincode)
            if(len(pincode)<6):
                flag_error=1
                return render_template('registration.html',error_display_pincode="block",
                    error_pincode="Error: Pincode. must be 10 digits long",
                    firstname=firstname,lastname=lastname,gender=gender,aadhaar=aadhaar,phone=phone,birthday=birthday)


        if(flag_error==0):
            error_display_firstname=error_display_lastname=error_display_gender=error_display_aadhaar =error_display_phone=error_display_pincode=error_display_dob=error_display_head="none"
        if(flag_error==1):
            return render_template('registration.html',error_display_head="block",
                    error_head="There are one or more errors in your form. Correct them and register again !",
                    firstname=firstname,lastname=lastname,gender=gender,aadhaar=aadhaar,phone=phone,birthday=birthday,pincode=pincode)



    making_global_aadhaar(aadhaar)

    '''cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT patient_id from patient')
    pid=cursor.fetchall()
    cursor.close()
    #print(pid)'''

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT aadhaar_uid from patient')
    uid=list(cursor.fetchall())
    cursor.close()
    print(uid)
    print(type(uid))
    
    if(len(uid)>0):

        for j in uid:
            if j.get('aadhaar_uid')==aadhaar:
                return render_template('registration.html',error="Error : Already a registered user ",firstname=firstname,lastname=lastname,gender=gender) 
            else: 
                id=random_n_digits(14)     
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO patient VALUES (%s, % s, % s, % s, % s, % s, % s, % s,%s,%s)',(id,firstname, lastname, gender , aadhaar, phone, birthday, pincode, total, screening,))
                mysql.connection.commit()
                msg='You have successfully registered !'
                break
                        
    else:
        id=random_n_digits(14)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO patient VALUES (%s,% s, % s, % s, % s, % s, % s, % s,%s,%s)',(id,firstname, lastname, gender , aadhaar, phone, birthday, pincode, total, screening))
        mysql.connection.commit()

    
    
    '''if(len(pid)>0 and len(uid)>0):

        for j in uid:
            if j.get('aadhaar_uid')==aadhaar:
                return render_template('registration.html',error="already a registered user ") 
            else:    
                for i in pid:
                    id=random_n_digits(14)
                    if(id==i):
                        continue
                    else:
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cursor.execute('INSERT INTO patient VALUES (%s, % s, % s, % s, % s, % s, % s, % s,%s,%s)',(id,firstname, lastname, gender , aadhaar, phone, birthday, pincode, total, screening,))
                        mysql.connection.commit()
                        msg='You have successfully registered !'
                        break
                        
    else:
        id=random_n_digits(14)
        cursor.execute('INSERT INTO patient VALUES (%s,% s, % s, % s, % s, % s, % s, % s,%s,%s)',(id,firstname, lastname, gender , aadhaar, phone, birthday, pincode, total, screening))
        mysql.connection.commit()'''
    
    cursor.execute('SELECT patient_id from patient WHERE aadhaar_uid=%s',[aadhaar])
    patient_id= cursor.fetchone()
    making_global_patient(patient_id.get('patient_id'))
    return render_template('question.html',patient_id=patient_id.get('patient_id'))

def random_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
    

@app.route('/submit', methods=['GET','POST'])
def ncd_rac():
    if request.method == "POST":
        total=0
        age=-1
        smoke=-1
        alcohol=-1
        waist=-1
        phy_act=-1
        fam_his=-1
        
        try:
            # age = int(request.form['age'])
            # smoke = int(request.form['smoke'])
            # alcohol = int(request.form['alcohol'])
            # waist = int(request.form['waist'])
            # phy_act = int(request.form['phy_act'])
            # fam_his = int(request.form['fam_his'])
            age = int(request.form.get('age'))
            smoke = int(request.form.get('smoke'))
            alcohol = int(request.form.get('alcohol'))
            waist = int(request.form.get('waist'))
            phy_act = int(request.form.get('phy_act'))
            fam_his = int(request.form.get('fam_his'))

        except Exception as e:
            print("Please answer all the questions.",e)
            return render_template('question.html',error="please answer all the questions",patient_id=patient_id)         
        

        total = age + smoke + alcohol + waist + phy_act + fam_his

        res=""
        screening=""
        
        if total>4:
            res="The person may be at higher risk of NCDs and needs to be prioritized for attending screening."
            screening ="yes"
        else:
            res="The person is not at risk of NCDs and doesn't need screening."
            screening ="no"

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE patient SET score =% s,screening =% s WHERE aadhaar_uid =% s',(total,screening,aadhaar))

    mysql.connection.commit()   

    return render_template('result.html',result=res,total=total, age=age,smoke=smoke,alcohol=alcohol,
                            waist=waist,phy_act=phy_act,fam_his=fam_his)              