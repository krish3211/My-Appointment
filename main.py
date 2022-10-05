from flask import Flask,render_template,request,session,redirect,url_for,flash
import database as db
app = Flask(__name__)
app.config['SECRET_KEY'] = "morpheius"

@app.route('/')
def Index():
    return render_template('index.html')
@app.route('/signin')
def Sigin():
    return render_template('signin.html')
@app.route('/Signin-form',methods=['POST','GET'])
def Sign_form():
    if request.method == 'POST':  
        session['Uname'] = request.form['username']
        session['Uemail']=request.form['email']
        session['Upass'] = request.form['password']
    insert=db.sign_from(session['Uname'],session['Uemail'],session['Upass'])
    ce=db.check_email(session['Uemail'])
    if ce == []:
        return render_template('registerform.html')
    if insert == '200':
        return render_template('registerform.html')
    return insert
@app.route('/Form',methods=['POST','GET'])
def form():
    fname= request.form['First_Name']
    lname= request.form['Last_Name']
    day= request.form['Birthday_day']
    month= request.form['Birthday_Month']
    year= request.form['Birthday_Year']
    email= request.form['Email_Id']
    phno= request.form['Mobile_Number']
    gender= request.form['Gender']
    address= request.form['Address']
    city= request.form['City']
    pincode= request.form['Pin_Code']
    state= request.form['State']
    country= request.form['Country']
    db.reg_form(fname,lname,day,month,year,email,phno,gender,address,city,pincode,state,country,g=session['Uemail'])
    return render_template('ulogin.html')
@app.route('/login',methods=['POST','GET'])
def login():
    if request.form['input'] == 'User':
        return render_template('ulogin.html')
    else:
        return render_template('Dlogin.html')
@app.route('/User-Home',methods=['POST','GET'])
def User_Home():
    if request.method == 'POST':    
        session['Uemail']=request.form['email']
        session['Upass'] = request.form['password']
    log=list(db.userlog(session['Uemail'],session['Upass']))
    if log == []:
        flash("Your email and Password is invaild \n Navigating back to Home")  
        return redirect(url_for('Index')) 
    a=log[0]
    session['id']=str(a[0])
    return render_template('home.html')

@app.route("/Doctor-Home",methods=['POST','GET'])
def Doctor_Home():
    if request.method == 'POST':    
        session['Dname']=request.form['Name']
        session['Dpass'] = request.form['password']
    key=db.Doctorlog(session['Dname'],session['Dpass'])
    if key == []:
        flash("Your email and Password is invaild \n Navigating back to Home")  
        return redirect(url_for('Index')) 
    return render_template('doctor_page.html')

@app.route('/D_P',methods=['POST','GET'])
def D_P():
    if request.method == 'POST': 
        session['cat']=request.form['category']
    pat=db.doc_pat(session['cat'])
    if pat==[]:
        return 'No Appointment \n <a href="./Doctor-Home">Back</a>'
    return render_template('Doc_pac.html',pat=pat)

@app.route('/Patient_pre',methods=['POST','GET'])
def Pat_pre():
    if request.method == 'POST': 
        cat=request.form['Patient']
        cat=list(map(str,cat.split()))
        session['id']=int(cat[0])
        session['date']=cat[1]
        session['time']=cat[2]
    return render_template('patient_pre.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    text=request.form['Prescription']
    update=db.submit(session['id'],session['date'],session['time'],session['cat'],text)
    if update == 'success':
        return redirect(url_for('D_P'))
    return 'error'

@app.route('/history')
def history():
    rows=db.table(session['id'])
    return render_template('History.html',rows=rows)

@app.route('/new-booking')
def new_booking():
    return render_template('newbooking.html')
@app.route('/process',methods=['POST','GET'])
def process():
    if request.method == 'POST': 
        name=request.form['Name']
        cat= request.form['category']
        date=request.form['date']
        time=request.form['Time']
    
    check_appo=db.check_appo(cat,date,time)
    if check_appo==[]:
        apply=db.apply_booking(name,cat,date,time,session['id'])
        return redirect(url_for('User_Home'))
    return 'This time already alloted'
@app.route('/Prescription',methods=['POST','GET'])
def Prescription():
    data = request.form['id']
    data=list(map(str,data.split()))
    id = int(data[0])
    cat= data[1]
    date=data[2]
    rows=db.fetch_report(id,cat,date)
    rows=rows[0]
    rows=rows[0]
    return render_template('prescription.html',date=date,cat=cat,text=rows)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
