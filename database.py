import email
import sqlite3 as sq

def userlog(eamil,password):
    con = sq.connect('database.db')
    cur = con.cursor()
    cur.execute(f"select * from user where Email = '{eamil}' And password = '{password}';")
    rows = cur.fetchall()
    return rows

def Doctorlog(name,password):
    con = sq.connect('database.db')
    cur = con.cursor()
    cur.execute(f"select * from Admit where username = '{name}' And password = '{password}';")
    rows = cur.fetchall()
    return rows 
def sign_from(name,email,password):
    con = sq.connect('database.db')
    cur = con.cursor()
    cur.execute(f"select Email from user;")
    rows = cur.fetchall()
    if (email,) not in rows:
        cur.execute(f"INSERT INTO user (Name,Email,password)VALUES ('{name}','{email}','{password}');")
        con.commit()
        return "200"
    return "Already exist email go back"
def reg_form(fname,lname,day,month,year,email,phno,gender,Address,city,pincode,state,country,g):
    con = sq.connect('database.db')
    cur=con.cursor()
    cur.execute(f"INSERT INTO user_full VALUES ('{fname}','{lname}',{day},'{month}',{year},'{email}',{phno},'{gender}','{Address}','{city}',{pincode},'{state}','{country}');")
    con.commit()
    cur.execute(f"UPDATE user SET Email='{email}' WHERE Email='{g}' ;")
    con.commit()
    return '200'
def check_email(email):
    con = sq.connect('database.db')
    cur = con.cursor()
    cur.execute(f"select email from user_full where email='{email}';")
    a=cur.fetchall()
    return a
def check_appo(cat,date,time):
    con = sq.connect('database.db')
    cur = con.cursor()
    cur.execute(f"SELECT category from Booking_users where date='{date}' AND time='{time}' AND category='{cat}';")
    a=cur.fetchall()
    return a
def apply_booking(name,cat,date,time,id):
    con = sq.connect('database.db')
    cur=con.cursor()
    cur.execute(f"INSERT INTO Booking_users VALUES ('{name}','{cat}','{date}','{time}','{id}','Pending','-');")
    con.commit()
    return '200'
def table(id):
    con = sq.connect('database.db')
    cur = con.cursor()
    cur.execute(f"SELECT * from Booking_users where id='{id}';")
    a=cur.fetchall()
    return a
def doc_pat(cat):
    con = sq.connect('database.db')
    cur = con.cursor()
    cur.execute(f"SELECT date,id,name,time FROM Booking_users WHERE category='{cat}' and Status='Pending' ORDER BY date ASC;")
    a=cur.fetchall()
    return a
def submit(id ,date,time,cat,text):
    con = sq.connect('database.db')
    cur=con.cursor()
    cur.execute(f"UPDATE Booking_users SET prescription='{text}', Status='Complete' WHERE id='{id}' and date='{date}' and category='{cat}' and Status='Pending' and time='{time}';")
    con.commit()
    return 'success'
def fetch_report(id,cat,date):
    con = sq.connect('database.db')
    cur = con.cursor()
    cur.execute(f"SELECT prescription from Booking_users WHERE id={id} and date='{date}' and  category='{cat}';")
    a=cur.fetchall()
    return a